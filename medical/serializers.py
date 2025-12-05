from rest_framework import serializers
from .models import MedicalHistory, PatientVital, PatientVisit


class MedicalHistorySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.get_user_name", read_only=True)
    patient_reg_no = serializers.CharField(source="patient.reg_no", read_only=True)


    class Meta:
        model = MedicalHistory
        fields = [
            "patient","patient_name", "patient_reg_no",
            "allergies", "chronic_conditions", "past_surgeries",
            "current_medications", "family_history",
            "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]



class PatientVitalSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.get_user_name", read_only=True)
    recorded_by_name = serializers.CharField(source="recorded_by.full_name", read_only=True)
    patient_card_no = serializers.CharField(source="patient.card_no", read_only=True)
    bmi = serializers.SerializerMethodField()

    class Meta:
        model = PatientVital
        fields = [
            "id", "patient", "patient_name",
            "temperature", "blood_pressure", "pulse_rate",
            "respiratory_rate", "weight", "height", "bmi",
            "recorded_by", "recorded_at", "created_at", 
            "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_bmi(self, obj):
        try:
            return round(obj.bmi(), 2)
        except:
            return None


class PatientVisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.full_name", read_only=True)
    patient_card_no = serializers.CharField(source="patient.card_no", read_only=True)


    class Meta:
        model = PatientVisit
        fields = [
            "id", "patient", "patient_name",
            "doctor", "doctor_name",
            "visit_reason", "diagnosis",
            "prescribed_medications", "patient_card_no",
            "visit_date", "follow_up_date",
            "created_at", "updated_at"
        ]
        read_only_fields = ["visit_date", "created_at", "updated_at"]
    
    def get_doctor_name(self, obj):
        if obj.doctor:
            u = obj.doctor.user
            return f"{u.first_name} {u.surname} {u.last_name} ({u.email})"
        return None





    # def get_doctor_name(self, obj):
    #     if obj.doctor:
    #         u = obj.doctor.user
    #         return f"{u.first_name} {u.surname} {u.last_name} ({u.email})"
    #     return None
