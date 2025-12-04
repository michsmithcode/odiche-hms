from rest_framework import serializers
from .models import MedicalHistory, PatientVital, PatientVisit


class MedicalHistorySerializer(serializers.ModelSerializer):
    patient_card_no = serializers.CharField(source="patient.card_no", read_only=True)

    class Meta:
        model = MedicalHistory
        fields = [
            "id", "patient", "patient_card_no",
            "condition", "description", "diagnosis_date", "created_at"
        ]
        read_only_fields = ["created_at"]


class PatientVitalSerializer(serializers.ModelSerializer):
    patient_card_no = serializers.CharField(source="patient.card_no", read_only=True)
    recorded_by_email = serializers.CharField(source="recorded_by.email", read_only=True)

    class Meta:
        model = PatientVital
        fields = [
            "id", "patient", "patient_card_no", "recorded_by", "recorded_by_email",
            "temperature", "blood_pressure", "heart_rate",
            "respiratory_rate", "weight", "height", "created_at"
        ]
        read_only_fields = ["created_at", "recorded_by"]



class PatientVisitSerializer(serializers.ModelSerializer):
    patient_card_no = serializers.CharField(source="patient.card_no", read_only=True)
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = PatientVisit
        fields = [
            "id", "patient", "patient_card_no", "doctor", "doctor_name",
            "visit_date", "symptoms", "diagnosis", "treatment", "follow_up_date"
        ]
        read_only_fields = ["visit_date"]

    def get_doctor_name(self, obj):
        if obj.doctor:
            u = obj.doctor.user
            return f"{u.first_name} {u.surname} {u.last_name} ({u.email})"
        return None
