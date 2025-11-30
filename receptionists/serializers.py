from rest_framework import serializers
from .models import ReceptionistProfile


class ReceptionistSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = ReceptionistProfile
        fields = "__all__"
        read_only_fields = ["employee_id", "created_at", "updated_at"]
