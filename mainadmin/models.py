from django.db import models
from django.conf import settings
from accounts.mixins import EmployeeIDMixin


class MainAdminProfile(EmployeeIDMixin, models.Model):
    prefix = "MA"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name="main_admin_profile"
    )

    office_title = models.CharField(max_length=100, default="System Administrator")
    permissions_level = models.CharField(
        max_length=50,
        default="super", 
        help_text="Defines the access level: super, audit, read-only"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=True) 

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Administrator {self.user.first_name} {self.user.last_name}"

