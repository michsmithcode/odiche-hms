from django.shortcuts import render

# Create your views here.




#============= Permission access control for receptionists
# from permissions.decorators import permission_required

# #Receptionist
# @permission_required("can_register_patient")
# def register_patient(request):
#     return Response({"message": "Receptionist registered patient"})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Receptionist
from .serializers import ReceptionistSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_receptionist_profile(request):
    """Retrieve the logged-in receptionist's profile."""

    try:
        receptionist = Receptionist.objects.get(user=request.user)
    except Receptionist.DoesNotExist:
        return Response({"error": "Receptionist profile not found"}, status=404)

    serializer = ReceptionistSerializer(receptionist)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_receptionist_profile(request):
    """Create a receptionist profile for the logged-in user."""
    data = request.data.copy()
    data["user"] = request.user.id

    # prevent duplicate profile
    if Receptionist.objects.filter(user=request.user).exists():
        return Response({"error": "Profile already exists"}, status=400)

    serializer = ReceptionistSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_receptionist_profile(request):
    try:
        receptionist = Receptionist.objects.get(user=request.user)
    except Receptionist.DoesNotExist:
        return Response({"error": "Receptionist profile not found"}, status=404)

    serializer = ReceptionistSerializer(
        receptionist, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_receptionist_profile(request):
    try:
        receptionist = Receptionist.objects.get(user=request.user)
    except Receptionist.DoesNotExist:
        return Response({"error": "Receptionist profile not found"}, status=404)

    receptionist.delete()
    return Response({"message": "Profile deleted"}, status=200)

