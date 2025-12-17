from rest_framework import serializers
from .models import Admission, Treatment


class AdmissionSerializer(serializers.ModelSerializer):
    patient_display = serializers.SerializerMethodField(read_only=True)
    doctor_display = serializers.SerializerMethodField(read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = Admission
        fields = [
            "id",
            "patient",
            "patient_display",
            "admitted_on",
            "expected_discharge_date",
            "discharged_on",
            "ward",
            "ward_name",
            "room_number",
            "attending_doctor",
            "doctor_display",
            "diagnosis",
            "status",
            "notes",
        ]
        read_only_fields = ["admitted_on", "discharged_on"]

    def get_patient_display(self, obj):
        if obj.patient:
            u = obj.patient.user
            return f"{u.first_name} {u.last_name} - {obj.patient.reg_no}"
        return None

    def get_doctor_display(self, obj):
        if obj.attending_doctor:
            u = obj.attending_doctor.user
            return f"Dr. {u.last_name}"
        return None


class TreatmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.__str__", read_only=True)
    admission_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Treatment
        fields = [
            "id",
            "admission",
            "admission_display",
            "date",
            "doctor",
            "doctor_name",
            "description",
            "procedure_name",
            "medication_prescribed",
            "notes",
        ]
        read_only_fields = ["date", "doctor"]

    def get_admission_display(self, obj):
        if obj.admission and obj.admission.patient:
            u = obj.admission.patient.user
            return f"{u.first_name} {u.last_name}"
        return None
