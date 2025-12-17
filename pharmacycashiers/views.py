# from django.shortcuts import render

# # Create your views here.
# # pharmacy_cashier/views.py
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Transaction, PharmacyCashierProfile
# from patients.models import PatientProfile
# from pharmarcist.models import Prescription
# from .serializers import TransactionSerializer

# from rest_framework.permissions import IsAdminUser


# #from rest_framework.decorators import api_view, permission_classes
# #from rest_framework.response import Response
# from rest_framework import status, permissions
# #from .models import PharmacyCashier
# from .serializers import PharmacyCashierProfileSerializer
# from .permissions import IsCashierOrAdmin  # custom permission





# #==============permission access control for cashiers=======
# from permissions.decorators import permission_required

# #Pharmacy Cashier
# @permission_required("can_record_payment")
# def cashier_record_payment(request):
#     return Response({"message": "Payment recorded by cashier"})



# # ============================
# # Self Profile CRUD (Cashier)
# # ============================

# @api_view(['GET', 'PATCH'])
# @permission_classes([permissions.IsAuthenticated, IsCashierOrAdmin])
# def cashier_profile(request):
#     try:
#         cashier = PharmacyCashierProfile.objects.get(user=request.user)
#     except PharmacyCashierProfile.DoesNotExist:
#         return Response({"error": "Cashier profile not found."}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = PharmacyCashierProfileSerializer(cashier)
#         return Response(serializer.data)

#     if request.method == "PATCH":
#         serializer = PharmacyCashierProfileSerializer(cashier, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ============================
# # Admin-Level CRUD (Cashier)
# # ============================

# @api_view(['GET', 'POST'])
# @permission_classes([permissions.IsAdminUser])
# def admin_cashier_list_create(request):
#     if request.method == "GET":
#         cashiers = PharmacyCashierProfile.objects.all()
#         serializer = PharmacyCashierProfileSerializer(cashiers, many=True)
#         return Response(serializer.data)

#     if request.method == "POST":
#         serializer = PharmacyCashierProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PATCH', 'DELETE'])
# @permission_classes([permissions.IsAdminUser])
# def admin_cashier_detail(request, pk):
#     try:
#         cashier = PharmacyCashierProfile.objects.get(pk=pk)
#     except PharmacyCashierProfile.DoesNotExist:
#         return Response({"error": "Cashier not found."}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = PharmacyCashierProfileSerializer(cashier)
#         return Response(serializer.data)

#     if request.method == "PATCH":
#         serializer = PharmacyCashierProfileSerializer(cashier, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == "DELETE":
#         cashier.delete()
#         return Response({"message": "Cashier deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



# # List transactions of logged-in cashier
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def cashier_transactions(request):
#     try:
#         cashier = PharmacyCashierProfile.objects.get(user=request.user)
#     except PharmacyCashierProfile.DoesNotExist:
#         return Response({"error": "Cashier profile not found"}, status=status.HTTP_404_NOT_FOUND)
#     transactions = Transaction.objects.filter(cashier=cashier)
#     serializer = TransactionSerializer(transactions, many=True)
#     return Response(serializer.data)


# # Create transaction by the Cashier
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def create_transaction(request):
#     try:
#         cashier = PharmacyCashierProfile.objects.get(user=request.user)
#     except PharmacyCashierProfile.DoesNotExist:
#         return Response({"error": "Cashier profile not found"}, status=status.HTTP_404_NOT_FOUND)

#     patient_id = request.data.get("patient")
#     prescription_id = request.data.get("prescription", None)

#     if not patient_id:
#         return Response({"error": "Patient is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         patient = PatientProfile.objects.get(pk=patient_id)
#     except PatientProfile.DoesNotExist:
#         return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

#     prescription = None
#     if prescription_id:
#         try:
#             prescription = Prescription.objects.get(pk=prescription_id)
#         except Prescription.DoesNotExist:
#             return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)

#     serializer = TransactionSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(cashier=cashier, patient=patient, prescription=prescription)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# #Performing CRUD by the Admin

# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def admin_list_transactions(request):
#     transactions = Transaction.objects.all()
#     serializer = TransactionSerializer(transactions, many=True)
#     return Response(serializer.data)

# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def admin_get_transaction(request, pk):
#     transaction = Transaction.objects.filter(pk=pk).first()
#     if not transaction:
#         return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = TransactionSerializer(transaction)
#     return Response(serializer.data)

# @api_view(["PUT", "PATCH"])
# @permission_classes([IsAdminUser])
# def admin_update_transaction(request, pk):
#     transaction = Transaction.objects.filter(pk=pk).first()
#     if not transaction:
#         return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = TransactionSerializer(transaction, data=request.data, partial=(request.method=="PATCH"))
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["DELETE"])
# @permission_classes([IsAdminUser])
# def admin_delete_transaction(request, pk):
#     transaction = Transaction.objects.filter(pk=pk).first()
#     if not transaction:
#         return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
#     transaction.delete()
#     return Response({"message": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
