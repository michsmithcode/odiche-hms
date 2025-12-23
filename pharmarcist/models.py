from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
#from accounts.employee_id import generate_employee_id
from django.db import models
from patients.models import PatientProfile
from accounts.mixins import EmployeeIDMixin

class PharmacistProfile(EmployeeIDMixin, models.Model):
    prefix = "PHARM"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacist_profile",
        primary_key=True
    )
    
    #employee_id = models.CharField(max_length=50, unique=True, editable=False)
    years_of_experience = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255, blank=True, null=True)
    shift = models.ForeignKey(Shift, max_length=50, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    #comfirmation of profile completion
    @property
    def is_profile_complete(self):
        required_fields = [
            self.address,
            self.qualifications,
            self.phone_number,
        ]
        return all(required_fields)
    
    
    def __str__(self):
        user = self.user
        full_name = f"Pharmacist {user.first_name} {user.surname} {user.last_name}".strip()
        return f"{full_name} ({user.email})"
    

    

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


  #NOT USED
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("PHARM", self.user.id)
    #     super().save(*args, **kwargs)
    
    