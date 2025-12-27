from django.db import models
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from ward.models import Ward, Bed
from django.conf import settings

class Admission(models.Model):
    STATUS_CHOICES = [
        ('admitted', 'ADMITTED'),
        ('discharged', 'DISCHARGED'),
        ('transferred', 'TRANSFERRED'),
    ]

    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='admissions')
    admitted_on = models.DateTimeField(auto_now_add=True)
    expected_discharge_date = models.DateField(blank=True, null=True)
    discharged_on = models.DateTimeField(blank=True, null=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name="admissions")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="admissions")
    room_number = models.CharField(max_length=10, blank=True, null=True)
    attending_doctor = models.ForeignKey( DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients_admitted')
    diagnosis = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='admitted')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - {self.get_status_display()}"

    class Meta:
        ordering = ['-admitted_on']





class Treatment(models.Model):
    admission = models.ForeignKey(
        'Admission',  # from previous example
        on_delete=models.CASCADE,
        related_name='treatments'
    )
    date = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, #recheck
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='treatments_given'
    )
    description = models.TextField(help_text="Details of the treatment or procedure performed")
    notes = models.TextField(blank=True, null=True)

    # link medications, procedures, investigations, etc.
    procedure_name = models.CharField(max_length=255, blank=True, null=True)
    medication_prescribed = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment for {self.admission.patient} on {self.date.date()}"

    class Meta:
        ordering = ['-date']
        
        