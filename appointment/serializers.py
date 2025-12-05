# from rest_framework import serializers
# from .models import Appointment


# class AppointmentSerializer(serializers.ModelSerializer):
#     # This Returns the model’s __str__() output, from either Doctor, Patient, or Nurse
#     doctor_display = serializers.CharField(source="doctor.__str__", read_only=True)
#     patient_display = serializers.CharField(source="patient.__str__", read_only=True)
#     nurse_display = serializers.CharField(source="nurse.__str__", read_only=True)

#     class Meta:
#         model = Appointment
#         fields = [
#             "id",
#             "doctor", "doctor_display",
#             "patient", "patient_display",
#             "nurse", "nurse_display",
#             "appointment_date",
#             "status",
#             "created_at",
#         ]
#         read_only_fields = [
#             "created_at",
#             "doctor_display",
#             "patient_display",
#             "nurse_display",
#         ]



# class AppointmentSerializer(serializers.ModelSerializer):
#     # Nested / related fields
#     doctor_name = serializers.CharField(source="doctor.user.get_full_name", read_only=True)
#     doctor_email = serializers.EmailField(source="doctor.user.email", read_only=True)

#     patient_name = serializers.CharField(source="patient.user.get_full_name", read_only=True)
#     patient_email = serializers.EmailField(source="patient.user.email", read_only=True)

#     nurse_name = serializers.CharField(source="nurse.user.get_full_name", read_only=True)
#     nurse_email = serializers.EmailField(source="nurse.user.email", read_only=True)

#     class Meta:
#         model = Appointment
#         fields = [
#             "id",
#             "doctor",
#             "doctor_name",
#             "doctor_email",
#             "patient",
#             "patient_name",
#             "patient_email",
#             "nurse",
#             "nurse_name",
#             "nurse_email",
#             "appointment_date",
#             "status",
#             "created_at",
#         ]
#         read_only_fields = [
#             "doctor_name",
#             "doctor_email",
#             "patient_name",
#             "patient_email",
#             "nurse_name",
#             "nurse_email",
#             "created_at",
#         ]
