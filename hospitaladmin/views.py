from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from doctors.models import DoctorProfile
from doctors.serializers import DoctorProfileSerializer


#====================
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import HospitalAdminProfile
from .serializers import HospitalAdminProfileSerializer


#Hospital_admin
@permission_required("can_manage_users")
def manage_staff(request):
    return Response({"message": "Hospital Admin managing staff"})



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_hospital_admin_profile(request):
    """
    Create Hospital Admin profile for logged-in user.
    """

    if hasattr(request.user, "hospital_admin_profile"):
        return Response(
            {"error": "Hospital admin profile already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = HospitalAdminProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hospital_admin_self_profile(request):
    """
    Retrieve logged-in hospital admin profile.
    """

    try:
        profile = request.user.hospital_admin_profile
    except HospitalAdminProfile.DoesNotExist:
        return Response(
            {"error": "Hospital admin profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = HospitalAdminProfileSerializer(profile)
    return Response(serializer.data)



@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_hospital_admin_profile(request):
    """
    Update logged-in hospital admin profile.
    """

    try:
        profile = request.user.hospital_admin_profile
    except HospitalAdminProfile.DoesNotExist:
        return Response(
            {"error": "Hospital admin profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = HospitalAdminProfileSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_hospital_admin(request, user_id):
    """
    Verify a hospital admin profile.
    """

    try:
        profile = HospitalAdminProfile.objects.get(user_id=user_id)
    except HospitalAdminProfile.DoesNotExist:
        return Response(
            {"error": "Hospital admin not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    profile.is_verified = True
    profile.save()

    return Response({"message": "Hospital admin verified successfully."})






# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def admin_list_doctors(request):
#     """
#     GET /admin/doctors/ - List all doctor profiles (Admin only)
#     """
#     doctors = Doctor.objects.all().select_related("user")
#     serializer = DoctorProfileSerializer(doctors, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def admin_get_doctor(request, doctor_id):
#     """
#     GET /admin/doctors/<id>/ - Retrieve specific doctor profile (Admin only)
#     """
#     try:
#         doctor = Doctor.objects.get(id=doctor_id)
#     except Doctor.DoesNotExist:
#         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = DoctorProfileSerializer(doctor)
#     return Response(serializer.data)


# @api_view(["PATCH"])
# @permission_classes([IsAdminUser])
# def admin_update_doctor(request, doctor_id):
#     """
#     PATCH /admin/doctors/<id>/update/ - Update doctor profile (Admin only)
#     """
#     try:
#         doctor = Doctor.objects.get(id=doctor_id)
#     except Doctor.DoesNotExist:
#         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

#     serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["DELETE"])
# @permission_classes([IsAdminUser])
# def admin_delete_doctor(request, doctor_id):
#     """
#     DELETE /admin/doctors/<id>/delete/ - Delete doctor profile (Admin only)
#     """
#     try:
#         doctor = Doctor.objects.get(id=doctor_id)
#         doctor.delete()
#         return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#     except Doctor.DoesNotExist:
#         return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
