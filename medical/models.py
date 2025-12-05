from django.db import models
from patients.models import PatientProfile
from doctors.models import DoctorProfile
# Create your models here.



class MedicalHistory(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="medical_history")
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    past_surgeries = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        u = self.patient.user
        full_name = f"{u.first_name} {u.last_name}".strip()
        return f"Medical History for {full_name} ({self.patient.reg_no})"
    
    
    
class PatientVital(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="vitals")
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_pressure = models.CharField(max_length=20)  # e.g., "120/80"
    pulse_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey('nurses.NurseProfile', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def bmi(self):
        return float(self.weight) / (float(self.height)/100)**2

    def __str__(self):
        return f"Vitals for {self.patient.card_no} at {self.recorded_at}"


class PatientVisit(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="visits")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    visit_reason = models.TextField()
    diagnosis = models.TextField(blank=True, null=True)
    prescribed_medications = models.TextField(blank=True, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Visit for {self.patient.card_no} - {self.visit_date}"

