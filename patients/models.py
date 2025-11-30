from django.db import models
from django.conf import settings
#from accounts.mixins import EmployeeIDMixin

GENDER_CHOICES = [
    ("male", "MALE"),
    ("female", "FEMALE"),
]


class PatientProfile(models.Model):
    #prefix = "PT"
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    card_no = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=11, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.card_no}"
