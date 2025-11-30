from rest_framework import serializers
from .models import NurseProfile

class NurseProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    
    class Meta:
        model = NurseProfile
        fields = [
            "email", 'first_name', "last_name", "role",
            "address", "qualifications", "shift", "is_verified", "created_at", "updated_at"
        ]
        read_only_fields = ['created_at']
