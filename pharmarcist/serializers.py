from rest_framework import serializers
from .models import PharmacistProfile

class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = "__all__"
        
        read_only_fields = ["user", "created_at", "updated_at"]
