#support for all users role

from django.db import models
from django.conf import settings
import uuid

SHIFT_TYPE = [
    ("regular", "Regular"),
    ("emergency", "Emergency"),
]

#Main_Admin Hopital_Admin Doctor Nurse Pharmacist Pharmacy_Cashier Lab Technician Receptionist Accountant, patient

ROLE_CHOICES = [
    ("main_admin", "MAIN ADMIN"),
    ("hospital_admin", "HOSPITAL ADMIN"),
    ("doctor", "DOCTOR"),
    ("nurse", "NURSE"),
    ("accountant", "ACCOUNTANT"),
    ("pharmacist", "PHARMACIST"),
    ("pharmacy_cashier", "PHARMACY CASHIER"),
    ("lab_technician", "LAB TECHNICIAN"),
    ("receptionist", "RECEPTIONIST"),
    ("patient", "PATIENT")
    
    
    ]




class Shift(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Assign shift to ANY USER
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shifts"
    )

    # Role of the user — prevents confusion
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    # Shift Date (single-day shift)
    date = models.DateField()

    # Time range
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Type of shift
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE, default="regular")

    # Who assigned the shift
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_shifts"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ("user", "date", "start_time", "end_time")

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return f"{full_name} ({self.role}) | {self.date} {self.start_time}-{self.end_time}"























# from django.db import models
# from django.conf import settings

# import uuid

# SHIFT_TYPE = [
#     ("regular", "Regular"),
#     ("emergency", "Emergency"),
# ]

# class Shift(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     nurse = models.ForeignKey(
#         "nurses.Nurse",
#         on_delete=models.CASCADE,
#         related_name="shifts"
#     )

#     # Supports multi-day shifts OR single day
#     date = models.DateField()

#     # Exact time ranges for shift
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     # Extra data for control
#     shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE, default="regular")
#     assigned_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="assigned_shifts"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["date", "start_time"]
#         unique_together = ("nurse", "date", "start_time", "end_time")
        
        
#     def __str__(self):
#         user = self.nurse.user     # access User model
#         full_name = f"Nurse {user.first_name} {user.surname} {user.last_name}".strip()
#         return f"{full_name} ({user.email}) | {self.date} {self.start_time} - {self.end_time}"




    # def __str__(self):
    #     return f"{self.nurse.user.get_full_name()} | {self.date} {self.start_time} - {self.end_time}"





# from django.conf import settings


# SHIFT_CHOICE = [
#     ("day", "DAY"),
#     ("night", "NIGHT")
# ]

# class Shift(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     shift = models.CharField(max_length=10, choices=SHIFT_CHOICE, default="day")
#     created_at = models.DateTimeField(auto_now_add=True)
    