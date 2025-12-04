from django.db import models
from django.conf import settings


class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    card_no = models.CharField(max_length=20, unique=True)
    reg_no = models.CharField(max_length=20, unique=True)
    file_folder_no = models.CharField(max_length=20, unique=True, editable=False)
   
    date_of_birth = models.DateField()
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=11, blank=True, null=True)
    emergency_contact_email= models.EmailField(unique=True, max_length=255, blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reg_no}"
    