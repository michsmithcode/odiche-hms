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
def list_admissions(request):
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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def discharge_patient(request, admission_id):
    try:
        admission = Admission.objects.get(id=admission_id)
    except Admission.DoesNotExist:
        return Response({"error": "Admission not found"}, status=404)

    admission.status = "discharged"
    admission.discharged_on = timezone.now()
    admission.save()

    return Response({
        "message": "Patient discharged successfully",
        "admission": AdmissionSerializer(admission).data
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_treatment(request):
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
