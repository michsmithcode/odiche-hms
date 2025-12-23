# from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import LabTechnicianProfile
from .serializers import LabTechnicianProfileSerializer



# #===================== Permission access control for labtechnician
from permissions.decorators import permission_required

#Lab Technician
@permission_required("can_upload_lab_result")
def upload_lab_results(request):
    return Response({"message": "Lab result uploaded"})



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_labtechnician_profile(request):
    """
    Create lab technician profile for logged-in user.
    """

    if hasattr(request.user, "labtechnician_profile"):
        return Response(
            {"error": "Lab technician profile already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = LabTechnicianProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def labtechnician_self_profile(request):
    """
    Retrieve logged-in lab technician profile.
    """

    try:
        profile = request.user.labtechnician_profile
    except LabTechnicianProfile.DoesNotExist:
        return Response(
            {"error": "Lab technician profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LabTechnicianProfileSerializer(profile)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_labtechnician_profile(request):
    """
    Update logged-in lab technician profile.
    """

    try:
        profile = request.user.labtechnician_profile
    except LabTechnicianProfile.DoesNotExist:
        return Response(
            {"error": "Lab technician profile not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LabTechnicianProfileSerializer(
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
def verify_labtechnician(request, user_id):
    """
    Verify a lab technician profile.
    """

    try:
        profile = LabTechnicianProfile.objects.get(user_id=user_id)
    except LabTechnicianProfile.DoesNotExist:
        return Response(
            {"error": "Lab technician not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    profile.is_verified = True
    profile.save()

    return Response({"message": "Lab technician verified successfully."})
