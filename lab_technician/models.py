from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
#from accounts.employee_id import generate_employee_id
from accounts.mixins import EmployeeIDMixin

class LabTechnicianProfile(EmployeeIDMixin, models.Model):
    prefix = "LAB"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="labtechnician_profile"
    )
    employee_id = models.CharField(max_length=50, unique=True, editable=False)
    address = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#NOT USED
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("LAB", self.user.id)
    #     super().save(*args, **kwargs)

    def __str__(self):
        full_name = f"LabTech {self.user.first_name} {self.user.last_name}".strip()
        return f"{full_name} ({self.user.email})"
