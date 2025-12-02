# from django.db import models

# # Create your models here.
# from django.db import models
# from django.utils import timezone
# #from accounts.models import PatientProfile, PharmacyCashierProfile, AccountantProfile
# #from .utils import generate_invoice_number



# class Billing(models.Model):
#     visit = models.OneToOneField(PatientVisit, on_delete=models.CASCADE, related_name="billing")
#     consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     medication_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     is_paid = models.BooleanField(default=False)

#     def calculate_total(self):
#         self.total_bill = self.consultation_fee + self.medication_fee + self.lab_fee
#         self.save()

#     def __str__(self):
#         return f"Billing for Visit #{self.visit.id}"



# class Transaction(models.Model):
#     PAYMENT_METHODS = (
#         ('cash', 'Cash'),
#         ('pos', 'POS'),
#         ('transfer', 'Bank Transfer'),
#     )

#     invoice_number = models.CharField(max_length=50, unique=True, editable=False)
#     patient = models.ForeignKey(
#         PatientProfile,
#         on_delete=models.SET_NULL,
#         null=True, blank=True,
#         related_name="transactions"
#     )
#     cashier = models.ForeignKey(
#         PharmacyCashierProfile,
#         on_delete=models.SET_NULL,
#         null=True, blank=True,
#         related_name="handled_transactions"
#     )
#     accountant = models.ForeignKey(
#         AccountantProfile,
#         on_delete=models.SET_NULL,
#         null=True, blank=True,
#         related_name="verified_transactions"
#     )

#     description = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
#     is_verified = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateTimeField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.invoice_number:
#             self.invoice_number = generate_invoice_number()
#         super().save(*args, **kwargs)

#     def is_overdue(self):
#         return self.due_date and timezone.now() > self.due_date

#     def __str__(self):
#         return f"{self.invoice_number} - {self.patient}"

# class Payment(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
#     processed_by = models.ForeignKey(PharmacyCashierProfile, on_delete=models.SET_NULL, null=True)

