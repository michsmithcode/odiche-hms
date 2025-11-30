from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
from accounts.employee_id import generate_employee_id
from accounts.mixins import EmployeeIDMixin

SPECIALIZATION_CHOICES = [
    ("general_practitioner", "General Practitioner"),
    ("cardiologist", "Cardiologist"),
    ("dermatologist", "Dermatologist"),
    ("neurologist", "Neurologist"),
    ("pediatrician", "Pediatrician"),
    ("psychiatrist", "Psychiatrist"),
    ("surgeon", "Surgeon"),
    ("radiologist", "Radiologist"),
    ("orthopedic", "Orthopedic"),
    ("gynecologist", "Gynecologist"),
    ("other", "Other"),
]

class DoctorProfile(EmployeeIDMixin, models.Model):
    prefix = "DR"
    #employee_id = models.CharField(max_length=50, unique=True, editable=False, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name="doctor_profile" )
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    qualifications = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    available_time_from = models.TimeField(blank=True, null=True)
    available_time_to = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("DR", self.user.id)
    #         super().save(*args, **kwargs)
    
    
    def __str__(self):
        user = self.user
        full_name = f"Dr. {user.first_name} {user.surname}".strip()
        return f"{full_name} ({user.email})  ({self.specialization})"



class ValidLicense(models.Model):
    license_number = models.CharField(max_length=100, unique=True)
    holder_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_number

