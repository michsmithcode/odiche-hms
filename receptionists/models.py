from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
from accounts.mixins import EmployeeIDMixin

#handled auto generated ID in account.mixins
class ReceptionistProfile(EmployeeIDMixin, models.Model):
    prefix = "RC"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="receptionist_profile"
    )

    
    address = models.TextField(blank=True, null=True)
    shift = models.ForeignKey(Shift,  on_delete=models.SET_NULL, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    #comfirmation of profile completion
    @property
    def is_profile_complete(self):
        required_fields = [
            self.address,
            #self.qualifications,
            self.phone_number,
        ]
        return all(required_fields)
    




    def __str__(self):
        user = self.user
        full_name = f"Receptionist {user.first_name} {user.surname} {user.last_name}".strip()
        return f"{full_name} ({user.email})"

#NOT USEd
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("REC", self.user.id)
    #     super().save(*args, **kwargs)
