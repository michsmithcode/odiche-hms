from django.shortcuts import render
from permissions.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import PatientProfile
from .serializers import PatientProfileSerializer
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.utils import send_password_reset_link


User = get_user_model()

#Receptionist or admin
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_patient(request):
    """
    Receptionist or admin registers a patient without OTP verification. create custom user profile, send password setup link
    Each patient's card number generated via Utilsfile, is a patient unique No for easily identification while folder 
    number is for easy search by admin, recept, or any specialist authorized,
    just like Physical folder in the hospital shelves , Helps the records office locate the patient's physical file
         
    """
    email = request.data.get("email")
    if User.objects.filter(email=request.data.get("email")).exists():
        return Response(
        {"error": "A user with this email already exists."},
        status=status.HTTP_400_BAD_REQUEST
    )
    # Create the user
    user = User.objects.create_user(
        email=email,
        password=None,  # placeholder; patient will set password via email
        first_name=request.data.get("first_name"),
        surname=request.data.get("surname"),
        last_name=request.data.get("last_name"),
        state=request.data.get("state"),
        phone_number=request.data.get("phone_number"),
        gender=request.data.get("gender"),
        role="patient",
        is_active=True,
        is_otp_verified=True
    )

    #Create the user profile
    patient_profile_data = {
        #"user": user.id,
        "date_of_birth": request.data.get("date_of_birth"),
        "emergency_contact_name": request.data.get("emergency_contact_name"),
        "emergency_contact_number": request.data.get("emergency_contact_number"),
        "address": request.data.get("address"),
    }
    #Create a patient profile
    serializer = PatientProfileSerializer(data=patient_profile_data)
    if serializer.is_valid():
        serializer.save(user=user)
        
        #send password reset link to patient
        reset_link = send_password_reset_link(user)
        return Response({
            "message": "Patient registered successfully",
            "Notice": "A password-reset link has been emailed to this patient",
             "password_setup_link_for_postman_testing": reset_link,
            "user": {
                "email": user.email,
                "name": f"{user.first_name} {user.surname} {user.last_name}",
                "role": user.role,
            },
            "profile": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=400)



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


#Multiple search task funtion formating
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def search_patient(request):
#     q = request.query_params.get("q")

#     results = PatientProfile.objects.filter(
#         reg_no__icontains=q
#     ) | PatientProfile.objects.filter(
#         card_no__icontains=q
#     ) | PatientProfile.objects.filter(
#         file_folder_no__icontains=q
#     )

#     serializer = PatientProfileSerializer(results, many=True)
#     return Response(serializer.data)


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



#Patient permision
@permission_required("can_view_patient")
def patient_view_profile(request):
    return Response({"message": "Patient viewing own profile"})



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




@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_patient_list(request):
    patients = PatientProfile.objects.all()
    serializer = PatientProfileSerializer(patients, many=True)
    return Response(serializer.data)


#Performing patient CRUD By Admin
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



#Receptionist Dashboard view
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patient_dashboard(request):
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