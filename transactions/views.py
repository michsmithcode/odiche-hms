from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Billing, Invoice, Transaction, Payment
from .serializers import BillingSerializer, InvoiceSerializer, TransactionSerializer, PaymentSerializer



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    serializer = InvoiceSerializer(data=request.data)

    if serializer.is_valid():
        invoice = serializer.save(created_by=request.user)
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        transaction = serializer.save(
            cashier=request.user.pharmacycashier_profile
        )
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)

    transaction.is_verified = True
    transaction.accountant = request.user.accountant_profile
    transaction.save()

    transaction.invoice.is_paid = True
    transaction.invoice.save()

    return Response({"message": "Transaction verified"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_payment(request):
    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():
        payment = serializer.save(
            processed_by=request.user.pharmacycashier_profile
        )
        return Response(PaymentSerializer(payment).data, status=201)

    return Response(serializer.errors, status=400)
