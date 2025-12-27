import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

from patients.models import PatientProfile
from pharmacycashiers.models import PharmacyCashierProfile
from accountant.models import AccountantProfile
from medical.models import PatientVisit
from .transaction_utils import generate_invoice_number


class Billing(models.Model):
    visit = models.OneToOneField(PatientVisit, on_delete=models.CASCADE, related_name="billing")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medication_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_finalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        self.total_bill = (
            self.consultation_fee +
            self.medication_fee +
            self.lab_fee
        )
        self.save()

    def __str__(self):
        return f"Billing for Visit #{self.visit.id}"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    billing = models.OneToOneField(Billing, on_delete=models.CASCADE, related_name="invoice")
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, null=True)
    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    due_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.invoice_number
    
    def is_overdue(self):
        return self.due_date and timezone.now().date() > self.due_date
    
    def __str__(self):
         return f"{self.invoice_number} - {self.patient}"


PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("pos", "POS"),
        ("transfer", "Bank Transfer"),
    ]

class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="transactions")
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, null=True, related_name="transactions")
    cashier = models.ForeignKey(PharmacyCashierProfile, on_delete=models.SET_NULL, null=True, related_name="handled_transactions")
    accountant = models.ForeignKey(AccountantProfile, on_delete=models.SET_NULL, null=True, related_name="verified_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TXN - {self.invoice.invoice_number}"


class Payment(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="payment")
    processed_by = models.ForeignKey(PharmacyCashierProfile,on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.transaction.invoice.invoice_number}"



