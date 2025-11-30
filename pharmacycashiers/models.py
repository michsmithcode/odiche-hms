from django.db import models
from django.conf import settings
from shift_mgt.models import Shift
#from accounts.employee_id import generate_employee_id
from accounts.mixins import EmployeeIDMixin

class PharmacyCashierProfile(EmployeeIDMixin, models.Model):
    prefix = "PHC"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name="cashier_profile"
    )
    
   
    address = models.TextField(blank=True, null=True)
    shift = models.ForeignKey(Shift, max_length=50, on_delete=models.SET_NULL, blank=True, null=True,)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    can_process_payments = models.BooleanField(default=True)
    can_verify_prescriptions = models.BooleanField(default=True)
    
    
    #NOT USED
    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         self.employee_id = generate_employee_id("CASH", self.user.id)
    #     super().save(*args, **kwargs)
    
    #profile_picture = models.ImageField
    
    def __str__(self):
        user = self.user
        full_name = f"PharmacyCashier {user.first_name} {user.surname} {user.last_name}".strip()
        return f"{full_name} ({user.email})"



   
"""
NOT NEEDED taken care in the transactionapp
# #importing the relationship
# from django.db import models
# from django.utils import timezone
# from .models import PharmacyCashierProfile
# from patients.models import PatientProfile
# from pharmarcist.models import Prescription


# #[("cash", "Cash"), ("card", "Card"), ("insurance", "Insurance")],
# PAYMENT_CHOICES = [
#     ("cash", "Cash"),
#     ("card", "Card"),
#     ("insurance", "Insurance")
# ]

# #Generate a transaction /Invoice
# class Transaction(models.Model):
#     cashier = models.ForeignKey(
#         PharmacyCashierProfile,
#         on_delete=models.SET_NULL, null=True, blank=True,
#         related_name="transactions"
#     )
#     patient = models.ForeignKey(
#         PatientProfile,
#         on_delete=models.SET_NULL, null=True, blank=True,
#         related_name="transactions"
#     )
#     prescription = models.ForeignKey(
#         Prescription,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="transactions"
#     )
    
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(
#         max_length=20,
#         choices= PAYMENT_CHOICES,
#         default="cash"
#     )
#     date_paid = models.DateTimeField(default=timezone.now)
#     remarks = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.patient.first_name} - {self.amount_paid} by {self.cashier.user.get_full_name()}"

"""