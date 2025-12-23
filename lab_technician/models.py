from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
from accounts.mixins import EmployeeIDMixin

class LabTechnicianProfile(EmployeeIDMixin, models.Model):
    prefix = "LAB"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="labtechnician_profile"
    )
   
    address = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    years_of_experince = models.BigIntegerField(default=0) #Not migrated
    bio = models.TextField(blank=True, null=True)#Not migrated
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Confirmation of profile completion
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
        full_name = f"LabTech. {user.first_name} {user.surname}".strip()
        return f"{full_name} ({user.email})  ({self.qualifications})"
    
    
    # employee_id = models.CharField(max_length=50, unique=True, editable=False)
    
    # full_name = f"LabTech {self.user.first_name} {self.user.last_name}".strip()
        # return f"{full_name} ({self.user.email})"

#NOT USED
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("LAB", self.user.id)
    #     super().save(*args, **kwargs)
