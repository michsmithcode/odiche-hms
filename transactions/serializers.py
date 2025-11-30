# from rest_framework import serializers
# from .models import Transaction


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = "__all__"
#         read_only_fields = ["invoice_number", "cashier", "accountant"]


# class PatientTransactionHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ["invoice_number", "description", "amount", "payment_method", "created_at"]
