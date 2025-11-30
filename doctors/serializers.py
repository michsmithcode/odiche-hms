from rest_framework import serializers
from .models import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "email", "first_name", "last_name", "role",
            "specialization", "license_number", "years_of_experience",
            "qualifications", "bio", "shift", "is_verified", "available_time_from", "available_time_to", 
            "created_at", "updated_at"
        ]
        
        extra_kwargs = {
    "license_number": {"required": True},
}
        read_only_fields = ["created_at"]



#Licence Number Verification Serializer
from .models import ValidLicense
import re

class LicenseVerificationSerializer(serializers.Serializer):
    license_number = serializers.CharField()

    def validate_license_number(self, value):
        pattern = r"^(MDCN|MDC)(/[A-Z]+)?/\d{3,6}$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Invalid MDCN license format. Example: MDCN/RN/12345"
            )

        # Check if license exists in your internal list
        if not ValidLicense.objects.filter(license_number=value).exists():
            raise serializers.ValidationError(
                "This license number is not found in the official registry."
            )

        # Check if another doctor already used it
        if DoctorProfile.objects.filter(license_number=value).exists():
            raise serializers.ValidationError(
                "This license number is already registered for another doctor."
            )

        return value




# import re

# class DoctorProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = [
#             "specialization",
#             "license_number",
#             "years_of_experience",
#             "qualifications",
#             "bio",
#             "shift",
#             "available_time_from",
#             "available_time_to",
#         ]
        extra_kwargs = {
            "license_number": {"required": True},
        }

#     def validate_license_number(self, value):
#         """
#         Validate:
#         - Not empty
#         - Format is valid (e.g., MDCN format)
#         - Unique license number
#         """
#         if not value:
#             raise serializers.ValidationError("License number is required.")

#         # Example Nigerian medical license validation (you can edit as needed)
#         pattern = r"^[A-Za-z0-9\-\/]+$"
#         if not re.match(pattern, value):
#             raise serializers.ValidationError(
#                 "Invalid license number format. Only letters, numbers, '-' or '/' are allowed."
#             )

#         # Ensure license is unique
#         # During update: exclude self instance
#         doctor = self.context.get("doctor")

#         existing = Doctor.objects.filter(license_number=value)

#         if doctor:
#             existing = existing.exclude(user=doctor.user)

#         if existing.exists():
#             raise serializers.ValidationError("This license number is already registered.")

#         return value
