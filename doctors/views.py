from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import csrf_exempt

#from rest_framework.permissions import AllowAny

# #Used for testing
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def test_auth(request):
#     return Response({"message": "TEST OK"})
    


#This view verifies the doctor's unique license
from .serializers import LicenseVerificationSerializer

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def verify_license(request):
    """
    Doctor submits their license number.
    System verifies format + internal list + uniqueness.
    """

    user = request.user

    # Ensure user is a doctor
    if not hasattr(user, "doctor_profile"):
        return Response(
            {"error": "Only doctors can perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )

    doctor = user.doctor_profile

    serializer = LicenseVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    license_number = serializer.validated_data["license_number"]

    # Save license + verify doctor
    doctor.license_number = license_number
    doctor.is_verified = True
    doctor.save()

    return Response({
        "message": "License verified successfully.",
        "license_number": license_number,
        "is_verified": True
    }, status=status.HTTP_200_OK)


#========use this to grant permission for the doctor access control. This replaces the old method above======
from permissions.decorators import permission_required

# Doctor
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required("can_create_consultation")
def create_consultation(request):
    return Response({"message": "Doctor created consultation"})


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required("can_prescribe_medication")
def prescribe_drugs(request):
    return Response({"message": "Doctor you prescribed medication"})




@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_doctor_profile(request):
    """
    Retrieves logged-in doctor's profile
    """
    try:
        doctor = request.user.doctor_profile
        #doctor = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorProfileSerializer(doctor)
        response = serializer.data
        if not doctor.license_number:
            response["notice"] = "Please complete your doctor profile by entering your medical license number."

        return Response(response, status=status.HTTP_200_OK)
        #return Response(serializer.data, status=status.HTTP_200_OK)
    except DoctorProfile.DoesNotExist:
        return Response({"error": "Doctor profile not found"}, status=status.HTTP_404_NOT_FOUND)




from .serializers import DoctorProfileSerializer

@csrf_exempt
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_doctor_profile(request):
    # Each logged-in doctor has doctor_profile from OneToOne field
    try:
        doctor = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        return Response(
            {"error": "Doctor profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = DoctorProfileSerializer(
        doctor,
        data=request.data,
        partial=True,  # This gives a PATCH METHOD support
        context={"doctor": doctor}
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_doctor_profile(request):
    """
    Delete logged-in doctor's profile
    """
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        doctor.delete()
        return Response({"message": "Doctor profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except DoctorProfile.DoesNotExist:
        return Response({"error": "Doctor profile not found"}, status=status.HTTP_404_NOT_FOUND)



#managing doctors by the admin
@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_doctors(request):
    """
      List all doctor profiles by admin
    """
    doctors = DoctorProfile.objects.all().select_related("user")
    serializer = DoctorProfileSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Get a particular doctor
@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_get_doctor(request, doctor_id):
    """
     Retrieve specific doctor profile by admin
    """
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
    except DoctorProfile.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoctorProfileSerializer(doctor)
    return Response(serializer.data)

@csrf_exempt
@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def admin_update_doctor(request, doctor_id):
    """
    Update doctor profile by admin
    """
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
    except DoctorProfile.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def admin_delete_doctor(request, doctor_id):
    """
    Delete doctor profile by admin
    """
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        doctor.delete()
        return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except DoctorProfile.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

