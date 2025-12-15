from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    # This Returns the model’s __str__() output, from either Doctor or Patient
    #doctor_display = serializers.CharField(source="doctor.__str__", read_only=True)
    patient_display = serializers.CharField(source="patient.__str__", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "patient", "patient_display",
            "appointment_date",
            "status",
            "created_at", "updated_at",
        ]
        read_only_fields = ["patient_display","created_at", "updated_at", "status"]

