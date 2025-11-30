from rest_framework import serializers
from .models import AccountantProfile

class AccountantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountantProfile
        fields = [
            "user",
            "employee_id",
            "address",
            "qualifications",
            "shift",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["employee_id", "created_at", "updated_at", "user"]


#ACCOUNTING SECTION
from rest_framework import serializers
from .models import AccountantProfile, Invoice, Payment, TransactionLog


class AccountantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountantProfile
        fields = "__all__"



# class InvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = "__all__"



# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = "__all__"



# class TransactionLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TransactionLog
#         fields = "__all__"