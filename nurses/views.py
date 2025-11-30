from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, permissions
from .models import NurseProfile
from .serializers import NurseProfileSerializer
from django.views.decorators.csrf import csrf_exempt



#================Permission Access for the nurses===========

#Nurse
from permissions.decorators import permission_required


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required("can_record_vitals")
def record_vitals(request):
    return Response({"message": "Nurse recorded vitals"})
 

# from rest_framework import status, permissions
# from django.contrib.auth import get_user_model

#============================

#This function is handled by the admin Only


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_nurse(request, nurse_id):
    nurse = get_object_or_404(NurseProfile, pk=nurse_id)
    nurse.is_verified = True
    nurse.save()

    return Response({"message": "Nurse verified successfully"}, status=200)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_list_nurses(request):
    nurses = NurseProfile.objects.all()
    serializer = NurseProfileSerializer(nurses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_create_nurse(request):
    serializer = NurseProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Nurse created successfully", "nurse": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_update_nurse(request, nurse_id):
    try:
        nurse = NurseProfile.objects.get(id=nurse_id)
    except NurseProfile.DoesNotExist:
        return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = NurseProfileSerializer(nurse, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Nurse updated successfully", "nurse": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_delete_nurse(request, nurse_id):
    try:
        nurse = NurseProfile.objects.get(id=nurse_id)
    except NurseProfile.DoesNotExist:
        return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)
    nurse.delete()
    return Response({"message": "Nurse deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




#Nurse permission View, 
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def nurse_view_profile(request):
    """
    GET: Retrieve nurse's own profile
    PATCH: Update nurse's own profile
    """
    try:
        nurse = NurseProfile.objects.get(user=request.user)
    except NurseProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = NurseProfileSerializer(nurse)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = NurseProfileSerializer(nurse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "nurse": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




