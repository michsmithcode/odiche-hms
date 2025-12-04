from rest_framework import serializers
from .models import PatientProfile
from .utils import generate_reg_no, generate_file_folder_no, generate_card_number
from django.contrib.auth import get_user_model



User = get_user_model()
class PatientProfileSerializer(serializers.ModelSerializer):
    
    user_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)


    class Meta:
        model = PatientProfile
        fields = [
            "id", "user_name", "first_name","last_name", "role", "email",
            "reg_no", "card_no", "file_folder_no",
            "date_of_birth", "emergency_contact_name",
            "emergency_contact_number", "address",
            "is_verified", "created_at", "updated_at"
        ]
        read_only_fields = ["reg_no", "card_no", "file_folder_no", "is_verified", "created_at", "updated_at"]
        
        
    def get_user_name(self, obj):
        u = obj.user
        return f"{u.first_name} {u.surname} {u.last_name}".strip()




#To create a reg_no, folder, and card_no function
    def create(self, validated_data):
        reg_no = generate_reg_no()
        validated_data["reg_no"] = reg_no
        validated_data["card_no"] = validated_data["reg_no"]
        validated_data["file_folder_no"] = generate_file_folder_no()
        
        return PatientProfile.objects.create(**validated_data)
    