from django.db import models
from django.conf import settings
from accounts.mixins import EmployeeIDMixin

class HospitalAdminProfile(EmployeeIDMixin, models.Model):
    prefix = "HA"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name="hospital_admin_profile"
    )
    # office_number = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    qualifications = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        user = self.user
        full_name = f"Hospital Admin. {user.first_name} {user.surname}".strip()
        return f"{full_name} ({user.email})  ({self.specialization})"

    # def __str__(self):
    #     return f"Hospital Admin {self.user.first_name} {self.user.last_name}"