from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import PharmacyCashierProfile
from patients.models import PatientProfile
from pharmarcist.models import Prescription
from rest_framework.permissions import IsAdminUser
from .serializers import PharmacyCashierProfileSerializer

from .permissions import IsCashierOrAdmin  # custom permission



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_cashier(request, cashier_id):
    cashier = get_object_or_404(PharmacyCashierProfile, pk=cashier_id)
    cashier.is_verified = True
    cashier.save()

    return Response({"message": "Nurse verified successfully"}, status=200)



#==============permission access control for cashiers=======
from permissions.decorators import permission_required

#Pharmacy Cashier
@permission_required("can_record_payment")
def cashier_record_payment(request):
    return Response({"message": "Payment recorded by cashier"})




@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated, IsCashierOrAdmin])
def cashier_profile(request):
    try:
        cashier = PharmacyCashierProfile.objects.get(user=request.user)
    except PharmacyCashierProfile.DoesNotExist:
        return Response({"error": "Cashier profile not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PharmacyCashierProfileSerializer(cashier)
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = PharmacyCashierProfileSerializer(cashier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#ADMIN ONLY
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser])
def admin_cashier_list_create(request):
    if request.method == "GET":
        cashiers = PharmacyCashierProfile.objects.all()
        serializer = PharmacyCashierProfileSerializer(cashiers, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PharmacyCashierProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAdminUser])
def admin_cashier_detail(request, pk):
    try:
        cashier = PharmacyCashierProfile.objects.get(pk=pk)
    except PharmacyCashierProfile.DoesNotExist:
        return Response({"error": "Cashier not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PharmacyCashierProfileSerializer(cashier)
        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = PharmacyCashierProfileSerializer(cashier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        cashier.delete()
        return Response({"message": "Cashier deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

