from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()




class UserInviteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "surname",
            "last_name",
            "state",
            "phone_number",
            "gender",
            "role",
        ]

    def create(self, validated_data):
        email = validated_data.pop("email")
        role = validated_data.get("role")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": validated_data.get("first_name", ""),
                "surname": validated_data.get("surname", ""),
                "last_name": validated_data.get("last_name", ""),
                "state": validated_data.get("state", ""),
                "phone_number": validated_data.get("phone_number", None),
                "gender": validated_data.get("gender", None),
                "role": role,
                "is_active": False,
            },
        )
        
        try:
            group = Group.objects.get(name=role.capitalize())
            user.groups.add(group)
        except Group.DoesNotExist:
            pass  # fallback if group not found

        return user
        
    