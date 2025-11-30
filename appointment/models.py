from django.db import models
from django.conf import settings
from doctors.models import Doctor
from patients.models import PatientProfile
from nurses.models import NurseProfile


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name="appointments")
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, related_name="appointments")
    nurse = models.ForeignKey(NurseProfile, on_delete=models.SET_NULL, related_name="appointments", null=True, blank=True)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Appointment: {self.patient.user.first_name} with Dr. {self.doctor.user.last_name} on {self.appointment_date}"
