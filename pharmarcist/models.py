# from django.db import models
# from django.conf import settings

# class Pharmacist(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         primary_key=True, 
#         related_name="pharmacist_profile"
#     )

#     license_number = models.CharField(max_length=100, unique=True)
#     years_of_experience = models.PositiveIntegerField(default=0)
#     qualifications = models.TextField(blank=True, null=True)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Pharmacist {self.user.first_name} {self.user.last_name}"


from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
#from accounts.employee_id import generate_employee_id
from accounts.mixins import EmployeeIDMixin

class PharmacistProfile(EmployeeIDMixin, models.Model):
    prefix = "PHARM"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile",
        primary_key=True
    )
    
    employee_id = models.CharField(max_length=50, unique=True, editable=False)
    years_of_experience = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255, blank=True, null=True)
    shift = models.ForeignKey(Shift, max_length=50, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    #NOT USED
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("PHARM", self.user.id)
    #     super().save(*args, **kwargs)
    
    
    def __str__(self):
        user = self.user
        full_name = f"Pharmacist {user.first_name} {user.surname} {user.last_name}".strip()
        return f"{full_name} ({user.email})"
    
    
    
    # def __str__(self):
    #     return f"Pharmacist: {self.user.get_full_name() or self.user.email}"
    
    
    
    # pharmacy/models.py
from django.db import models
from patients.models import PatientProfile

#patient's Prescriptions
class Prescription(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="prescriptions")
    prescribed_by = models.CharField(max_length=150)  # doctor name or doctor profile FK
    medication_details = models.TextField()
    dosage_instructions = models.TextField()
    date_prescribed = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name}"

