from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Admission, Treatment
from .serializers import AdmissionSerializer, TreatmentSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admit_patient(request):
    serializer = AdmissionSerializer(data=request.data)
    if serializer.is_valid():
        admission = serializer.save()
        return Response(
            {
                "message": "Patient admitted successfully",
                "admission": AdmissionSerializer(admission).data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_patient_admissions(request):
    queryset = Admission.objects.all()

    status_param = request.GET.get("status")
    ward = request.GET.get("ward")
    patient = request.GET.get("patient")

    if status_param:
        queryset = queryset.filter(status=status_param)
    if ward:
        queryset = queryset.filter(ward_id=ward)
    if patient:
        queryset = queryset.filter(patient_id=patient)

    serializer = AdmissionSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def admission_detail(request, pk):
    try:
        admission = Admission.objects.get(pk=pk)
    except Admission.DoesNotExist:
        return Response({"error": "Admission not found"}, status=404)

    serializer = AdmissionSerializer(admission)
    return Response(serializer.data)

@api_view(["PATCH"])
def update_admission(request, pk):
    try:
        admission = Admission.objects.get(pk=pk)
    except Admission.DoesNotExist:
        return Response({"error": "Admission not found"}, status=404)

    serializer = AdmissionSerializer(admission, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def discharge_patient(request, admission_id):
    try:
        admission = Admission.objects.get(id=admission_id)
    except Admission.DoesNotExist:
        return Response({"error": "Admission not found"}, status=404)
    
    if admission.status == "discharged":
        return Response({"message": "Already discharged"})

    admission.status = "discharged"
    admission.discharged_on = timezone.now()
    
    if admission.bed:
        admission.bed.is_occupied = False
        admission.bed.save()
        
    admission.save()
    
    return Response({
        "message": "Patient discharged and bed released successfully",
        "admission": AdmissionSerializer(admission).data
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def administer_treatment(request):
    doctor = getattr(request.user, "doctor_profile", None)
    if not doctor:
        return Response({"error": "Only doctors can administer treatment."}, status=403)
    
    admission_id = request.data.get("admission")

    try:
        admission = Admission.objects.get(id=admission_id)
    except Admission.DoesNotExist:
        return Response({"error": "Invalid admission"}, status=400)
    
    
    #Unauthorized treatment after patient's discharged
    if admission.status != "admitted":
        return Response(
            {"error": "Cannot administer treatment after discharge"},
            status=403
        )

    serializer = TreatmentSerializer(data=request.data)
    if serializer.is_valid():
        treatment = serializer.save(doctor=request.user)
        return Response(
            {
                "message": "Treatment added successfully",
                "treatment": TreatmentSerializer(treatment).data
            },
            status=201
        )
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_treatments(request, admission_id):
    treatments = Treatment.objects.filter(admission_id=admission_id)
    serializer = TreatmentSerializer(treatments, many=True)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_treatment(request, pk):
    try:
        treatment = Treatment.objects.get(pk=pk)
    except Treatment.DoesNotExist:
        return Response({"error": "Treatment not found"}, status=404)

    serializer = TreatmentSerializer(treatment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

#Summary of patient admission

@api_view(["GET"])
def patient_admission_summary(request, pk):
    try:
        admission = Admission.objects.get(pk=pk)
    except Admission.DoesNotExist:
        return Response({"error": "Admission not found"}, status=404)

    treatments = admission.treatments.all()

    data = {
        "patient": str(admission.patient),
        "ward": admission.ward.name if admission.ward else None,
        "bed": str(admission.bed) if admission.bed else None,
        "doctor": str(admission.attending_doctor),
        "diagnosis": admission.diagnosis,
        "status": admission.status,
        "treatments": [
            {
                "date": t.date,
                "procedure": t.procedure_name,
                "medication": t.medication_prescribed,
                "notes": t.notes
            }
            for t in treatments
        ]
    }
    return Response(data)
