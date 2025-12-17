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



"""

===============================
       ACCOUNTING SYSTEM
===============================
"""



"""
NOT NEEDED its taken care in the transactionapp
# class Invoice(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     patient = models.ForeignKey(PatientProfile, null=True, on_delete=models.SET_NULL)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="invoices_created"
#     )

#     description = models.TextField()
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     is_paid = models.BooleanField(default=False)
#     due_date = models.DateField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Invoice {self.id} - {self.patient}"


# class Payment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     invoice = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL, related_name="payments")
#     amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_method = models.CharField(
#         max_length=50,
#         choices=[
#             ("cash", "Cash"),
#             ("card", "Card"),
#             ("transfer", "Bank Transfer"),
#             ("pos", "POS"),
#         ]
#     )
#     processed_by = models.ForeignKey(AccountantProfile, on_delete=models.SET_NULL, null=True)
#     payment_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Payment for Invoice {self.invoice.id}"


# class TransactionLog(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     action = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.action} - {self.timestamp}"
    

"""
