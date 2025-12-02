from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
#from accounts.employee_id import generate_employee_id
from accounts.mixins import EmployeeIDMixin

class NurseProfile(EmployeeIDMixin, models.Model):
    prefix = "NUR"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="nurse_profile"
    )
    
    address = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    shift = models.ForeignKey(Shift, max_length=50,  on_delete=models.SET_NULL, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_profile_complete(self):
        required_fields = [
            self.address,
            self.qualifications,
            self.phone_number,
        ]
        return all(required_fields)
    
    
    
    #NOT USED
    #This function generate an employee ID in human readable form
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("NUR", self.user.id)
    #     super().save(*args, **kwargs)
    
    
    def __str__(self):
        user = self.user
        full_name = f"Nurse {user.first_name} {user.surname} {user.last_name}".strip()
        return f"{full_name} ({user.email})"

    
   




    