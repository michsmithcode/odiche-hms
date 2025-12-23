from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt

from .models import AccountantProfile
from .serializers import AccountantProfileSerializer
from permissions.decorators import admin_only



#===================Permission access control for accountant======
from permissions.decorators import permission_required


#Accountant
@permission_required("can_view_financial_reports")
def finance_reports(request):
    return Response({"message": "Accountant viewing financial reports"})



@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accountant_profile(request):
    try:
        profile = AccountantProfile.objects.get(user=request.user)
        serializer = AccountantProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AccountantProfile.DoesNotExist:
        return Response({"error": "Accountant profile not found"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_accountant_profile(request):
    try:
        profile = AccountantProfile.objects.get(user=request.user)
    except AccountantProfile.DoesNotExist:
        return Response({"error": "Accountant profile not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountantProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, permissions.IsAdminUser])
@admin_only
def delete_accountant_profile(request, accountant_id):
    try:
        profile = AccountantProfile.objects.get(id=accountant_id)
        profile.delete()
        return Response({"message": "Accountant profile deleted"}, status=status.HTTP_204_NO_CONTENT)
    except AccountantProfile.DoesNotExist:
        return Response({"error": "Accountant profile not found"}, status=status.HTTP_404_NOT_FOUND)



@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@admin_only
def admin_list_accountants(request):
    profiles = AccountantProfile.objects.all()
    serializer = AccountantProfileSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@admin_only
def admin_get_accountant(request, accountant_id):
    try:
        profile = AccountantProfile.objects.get(id=accountant_id)
        serializer = AccountantProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AccountantProfile.DoesNotExist:
        return Response({"error": "Accountant profile not found"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
@admin_only
def admin_update_accountant(request, accountant_id):
    try:
        profile = AccountantProfile.objects.get(id=accountant_id)
    except AccountantProfile.DoesNotExist:
        return Response({"error": "Accountant profile not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountantProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def list_accountants(request):
    accountants = AccountantProfile.objects.all()
    serializer = AccountantProfileSerializer(accountants, many=True)
    return Response(serializer.data)

