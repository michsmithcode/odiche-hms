from rest_framework import serializers
from .models import HospitalAdminProfile


class HospitalAdminProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.SerializerMethodField()
    is_profile_complete = serializers.ReadOnlyField()

    class Meta:
        model = HospitalAdminProfile
        fields = [
            "user",
            "user_email",
            "full_name",
            "employee_id",
            "address",
            "years_of_experience",
            "qualifications",
            "bio",
            "is_verified",
            "created_at",
            "is_profile_complete",
        ]
        read_only_fields = [
            "user",
            "employee_id",
            "created_at",
            "is_verified",
        ]

    def get_full_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.surname}".strip()
