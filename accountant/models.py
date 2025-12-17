from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
#from accounts.employee_id import generate_employee_id
from accounts.mixins import EmployeeIDMixin

from patients.models import PatientProfile
#from django.utils import timezone
#import uuid


class AccountantProfile(EmployeeIDMixin, models.Model):
    prefix = "ACC"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="accountant_profile"
    )

    #employee_id = models.CharField(max_length=50, unique=True, editable=False)
    address = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)

    shift = models.OneToOneField(
        Shift,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#NOT USED
    # Auto-generate Accountant employee ID
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         # ACC prefix for accountants
    #         self.employee_id = generate_employee_id("ACC", self.user.id)
    #     super().save(*args, **kwargs)


    def __str__(self):
        user = self.user
        full_name = f"Accountant {user.first_name} {user.surname} {user.last_name}".strip()
        return f"{full_name} ({user.email})"


