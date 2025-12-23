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
            "years_of_experience",
            "bio",
            "shift",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["employee_id", "created_at", "updated_at", "user"]


# class AccountantProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountantProfile
#         fields = "__all__"

