from rest_framework import serializers
from .models import Transaction
from patients.models import PatientProfile
from pharmarcist.models import Prescription
from .models import PharmacyCashierProfile
from accounts.employee_id import generate_employee_id

#from accounts.models import CustomUser   # adjust path if needed


class PharmacyCashierProfileSerializer(serializers.ModelSerializer):
    # Pulling fields from the linked User model
    cashier_email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    employee_id = serializers.CharField(read_only=True)   # Auto-generated from user UUID

    class Meta:
        model = PharmacyCashierProfile
        fields = [
            "email",
            "employee_id",
            "cashier_email",
            "first_name",
            "last_name",
            "role",
            "address",
            "shift",
            "is_verified",
            "can_process_payments",
            "can_verify_prescriptions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
        
            "cashier_email",
            "full_name",
            "role",
            "created_at",
            "updated_at",
            "is_verified",
        ]
        
    
    # def __str__(self):
    #     return self.user.email

    # def get_full_name(self, obj):
    #     """Join first_name + surname + last_name dynamically."""
    #     user = obj.user
    #     return f"{user.first_name} {user.surname} {user.last_name}".strip()





# class TransactionSerializer(serializers.ModelSerializer):
#     cashier_email = serializers.EmailField(source="cashier.user.email", read_only=True)
#     patient_name = serializers.CharField(source="patient.__str__", read_only=True)
#     prescription_info = serializers.CharField(source="prescription.__str__", read_only=True)

#     class Meta:
#         model = Transaction
#         fields = [
#             "id", "cashier_email", "patient", "patient_name",
#             "prescription", "prescription_info",
#             "amount_paid", "payment_method", "date_paid", "remarks", "created_at"
#         ]
#         read_only_fields = ["cashier_email", "patient_name", "prescription_info", "created_at"]