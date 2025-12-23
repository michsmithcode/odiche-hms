from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from admmit_treatements.models import Admission
from lab_technician.models import LabTechnicianProfile


class LabTest(models.Model):
    STATUS_CHOICES = [
        ("pending", "PENDING"),
        ("in_progress", "IN PROGRESS"),
        ("completed", "COMPLETED"),
        ("cancelled", "CANCELLED"),
    ]

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="lab_tests"
    )
    admission = models.ForeignKey(
        Admission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lab_tests"
    )
    ordered_by = models.ForeignKey(
        DoctorProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lab_tests_ordered"
    )
    test_name = models.CharField(max_length=255)
    clinical_notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} - {self.patient}"


class LabTestResult(models.Model):
    lab_test = models.OneToOneField(
        LabTest,
        on_delete=models.CASCADE,
        related_name="result"
    )
    technician = models.ForeignKey(
        LabTechnicianProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="results_uploaded"
    )

    result_summary = models.TextField()
    result_file = models.FileField(
        upload_to="lab_results/",
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.lab_test.test_name}"
