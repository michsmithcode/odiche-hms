from django.db import models
from django.conf import settings


GENDER_CHOICES = [
    ("male", "MALE"),
    ("female", "FEMALE"),
]


class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    card_no = models.CharField(max_length=10, unique=True)
    reg_no = models.CharField(max_length=20, unique=True)
    file_folder_no = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email= models.EmailField(unique=True, max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact_email= models.EmailField(unique=True, max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reg_no}"


from django.db import models
from patients.models import PatientProfile
from doctors.models import DoctorProfile

class MedicalHistory(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name="medical_history")
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    past_surgeries = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical History for {self.patient.first_name} {self.patient.last_name}"
    
    
    
class PatientVital(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="vitals")
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_pressure = models.CharField(max_length=20)  # e.g., "120/80"
    pulse_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey('nurses.Nurse', on_delete=models.SET_NULL, null=True)

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

    def __str__(self):
        return f"Visit for {self.patient.card_no} - {self.visit_date}"

