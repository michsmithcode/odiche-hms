from rest_framework import serializers
from .models import LabTechnicianProfile


class LabTechnicianProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.SerializerMethodField()
   # is_profile_complete = serializers.ReadOnlyField()

    class Meta:
        model = LabTechnicianProfile
        fields = [
            "user",
            "user_email",
            "full_name",
            "employee_id",
            "address",
            "qualifications",
            "years_of_experince",
            "bio",
            "shift",
            "is_verified",
            "created_at",
            "updated_at",
            #"is_profile_complete",
        ]
        read_only_fields = [
            "user",
            "employee_id",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def get_full_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.surname}".strip()
