from django.shortcuts import render
from permissions.decorators import permission_required

# Create your views here.



#Patient
@permission_required("can_view_patient")
def patient_self_profile(request):
    return Response({"message": "Patient viewing own profile"})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import PatientProfile
from .serializers import PatientProfileSerializer
from .utils import generate_card_number, generate_folder_no
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

# =======================================
# Receptionist Creates Patient
# =======================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_patient(request):
    """
    Receptionist registers a new patient and auto-generates card_no.
    """
    serializer = PatientProfileSerializer(data=request.data)
    """card number a patient unique No for easily identification while folder number is for easy search by admin, recep, or any specialist,
        just like Physical folder in the hospital shelves , Helps the records office locate the patient's physical file"""
    if serializer.is_valid():
        serializer.save(
            user=request.user,  # receptionist account that created the record
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_verify_patient(request, pk):
    try:
        patient = PatientProfile.objects.get(pk=pk)
    except PatientProfile.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)

    if patient.is_verified:
        return Response({"message": "Already verified"}, status=400)

    patient.is_verified = True
    patient.save()

    return Response({"message": "Patient verified successfully"})


@api_view(["GET"])
def search_by_reg_no(request):
    reg_no = request.GET.get("reg_no")
    if not reg_no:
        return Response({"error": "reg_no is required"}, status=400)

    try:
        patient = PatientProfile.objects.get(reg_no=reg_no)
        return Response(PatientProfileSerializer(patient).data)
    except PatientProfile.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)

@api_view(["GET"])
def search_by_folder(request):
    folder_no = request.GET.get("file_folder_no")
    if not folder_no:
        return Response({"error": "file_folder_no is required"}, status=400)

    try:
        patient = PatientProfile.objects.get(file_folder_no=folder_no)
        return Response(PatientProfileSerializer(patient).data)
    except PatientProfile.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_patient_by_card(request):
    card_no = request.GET.get("card_no")

    if not card_no:
        return Response({"error": "card_no parameter is required"}, status=400)

    try:
        patient = PatientProfile.objects.get(card_no=card_no)
    except PatientProfile.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)

    serializer = PatientProfileSerializer(patient)
    return Response(serializer.data)


#Applying pagination
class PatientPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_patients(request):
    patients = PatientProfile.objects.all().order_by("-created_at")
    
    paginator = PatientPagination()
    paginated = paginator.paginate_queryset(patients, request)
    
    serializer = PatientProfileSerializer(paginated, many=True)
    return paginator.get_paginated_response(serializer.data)



# Patient Self Profile (View Only)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patient_self_view(request):
    try:
        profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)

    serializer = PatientProfileSerializer(profile)
    return Response(serializer.data)


#Receptionist Dashboard
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def receptionist_dashboard(request):
    total_patients = PatientProfile.objects.count()
    verified = PatientProfile.objects.filter(is_verified=True).count()
    unverified = total_patients - verified

    today = timezone.now().date()
    today_reg = PatientProfile.objects.filter(created_at__date=today).count()

    male = PatientProfile.objects.filter(gender="male").count()
    female = PatientProfile.objects.filter(gender="female").count()

    data = {
        "total_patients": total_patients,
        "verified_patients": verified,
        "unverified_patients": unverified,
        "today_registered": today_reg,
        "male": male,
        "female": female,
    }

    return Response(data)


# =======================================
# Admin — List Patients
# =======================================
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_patient_list(request):
    patients = PatientProfile.objects.all()
    serializer = PatientProfileSerializer(patients, many=True)
    return Response(serializer.data)



# =======================================
# Admin — Retrieve / Update / Delete Patient
# =======================================
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_patient_detail(request, pk):
    try:
        patient = PatientProfile.objects.get(pk=pk)
    except PatientProfile.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)

    if request.method == "GET":
        serializer = PatientProfileSerializer(patient)
        return Response(serializer.data)

    if request.method == "PATCH": 
        serializer = PatientProfileSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        patient.delete()
        return Response({"message": "Patient deleted"}, status=204)


