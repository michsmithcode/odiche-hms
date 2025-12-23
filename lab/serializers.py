from rest_framework import serializers
from .models import LabTest, LabTestResult


class LabTestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.user.get_full_name",
        read_only=True
    )
    ordered_by_name = serializers.CharField(
        source="ordered_by.user.get_full_name",
        read_only=True
    )

    class Meta:
        model = LabTest
        fields = "__all__"
        read_only_fields = ["status", "ordered_at"]


class LabTestResultSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(
        source="lab_test.test_name",
        read_only=True
    )

    class Meta:
        model = LabTestResult
        fields = "__all__"
        read_only_fields = ["technician", "is_verified", "created_at"]
