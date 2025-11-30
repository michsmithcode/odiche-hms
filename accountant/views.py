from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from .models import AccountantProfile
from .serializers import AccountantProfileSerializer
from permissions.decorators import admin_only



#===================Permission access control for accountant======
# from permissions.decorators import permission_required
# #Accountant
# @permission_required("can_view_financial_reports")
# def finance_reports(request):
#     return Response({"message": "Accountant viewing financial reports"})




# ---------------------------------------------------------
# GET own accountant profile
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# UPDATE own profile
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# DELETE profile (Admin only)
# ---------------------------------------------------------
@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@admin_only
def delete_accountant_profile(request, accountant_id):
    try:
        profile = AccountantProfile.objects.get(id=accountant_id)
        profile.delete()
        return Response({"message": "Accountant profile deleted"}, status=status.HTTP_204_NO_CONTENT)
    except AccountantProfile.DoesNotExist:
        return Response({"error": "Accountant profile not found"}, status=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------
# ADMIN: List All Accountants
# ---------------------------------------------------------
@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@admin_only
def admin_list_accountants(request):
    profiles = AccountantProfile.objects.all()
    serializer = AccountantProfileSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------------------------------
# ADMIN: Get Single Accountant
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# ADMIN: Update Accountant
# ---------------------------------------------------------
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


#ACCOUNTING SECTION
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import AccountantProfile, Invoice, Payment, TransactionLog
from .serializers import (
    AccountantProfileSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    TransactionLogSerializer
)
from django.shortcuts import get_object_or_404


"""
================================
    ACCOUNTANT PROFILE VIEWS
================================
"""


@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def create_accountant(request):
    serializer = AccountantProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Log
        TransactionLog.objects.create(
            action="Created accountant profile",
            user=request.user
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def list_accountants(request):
    accountants = AccountantProfile.objects.all()
    serializer = AccountantProfileSerializer(accountants, many=True)
    return Response(serializer.data)



"""
============================
        INVOICES
============================
"""

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_invoice(request):
    serializer = InvoiceSerializer(data=request.data)

    if serializer.is_valid():
        invoice = serializer.save(created_by=request.user)

        TransactionLog.objects.create(
            action="Created invoice",
            amount=invoice.amount,
            user=request.user
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
============================
        PAYMENTS
============================
"""

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def make_payment(request):
    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():
        payment = serializer.save()

        # Mark invoice as paid if full amount is paid
        invoice = payment.invoice
        total_paid = sum([p.amount_paid for p in invoice.payments.all()])

        if total_paid >= invoice.amount:
            invoice.is_paid = True
            invoice.save()

        # Log
        TransactionLog.objects.create(
            action="Processed payment",
            amount=payment.amount_paid,
            user=request.user
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



