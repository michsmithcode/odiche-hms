from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import MedicalHistory, PatientVital, PatientVisit, PatientProfile
from .serializers import (
    MedicalHistorySerializer,
    PatientVitalSerializer,
    PatientVisitSerializer
)


#Medical Hostory
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def medical_history_list_create(request):
    if request.method == "GET":
        history = MedicalHistory.objects.all()
        serializer = MedicalHistorySerializer(history, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = MedicalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def medical_history_detail(request, pk):
    try:
        record = MedicalHistory.objects.get(pk=pk)
    except MedicalHistory.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MedicalHistorySerializer(record)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = MedicalHistorySerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#patient vitals CRUD
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patient_vital_list_create(request):
    if request.method == "GET":
        vitals = PatientVital.objects.all()
        serializer = PatientVitalSerializer(vitals, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PatientVitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recorded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


#Vital details
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def patient_vital_detail(request, pk):
    try:
        vital = PatientVital.objects.get(pk=pk)
    except PatientVital.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PatientVitalSerializer(vital)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = PatientVitalSerializer(vital, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        vital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Patient visit list
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patient_visit_list_create(request):
    if request.method == "GET":
        visits = PatientVisit.objects.all()
        serializer = PatientVisitSerializer(visits, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PatientVisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # doctor can be selected or auto-assigned later
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)



#Visit details
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def patient_visit_detail(request, pk):
    try:
        visit = PatientVisit.objects.get(pk=pk)
    except PatientVisit.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PatientVisitSerializer(visit)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = PatientVisitSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "DELETE":
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
