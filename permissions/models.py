from django.db import models
from django.conf import settings
import uuid


class Permission(models.Model):
    """
    Basic permission like: can_dispense_drugs, can_add_patient, can_view_records, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code


class HospitalRole(models.Model):
    """
    Roles inside the hospital: Admin, Doctor, Nurse, Pharmacist, Lab Technician, patient, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)   # e.g. "Pharmacist"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """
    Mapping: Role → Permissions
    Example:
        Pharmacist → [can_dispense_drugs, can_view_drugs]
        Doctor → [can_create_appointment, can_view_patient]
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(HospitalRole, on_delete=models.SET_NULL, null=True, blank=True, related_name="permissions")
    permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'permission')  # No duplicate permissions for a role

    def __str__(self):
        return f"{self.role.name} -> {self.permission.code}"
    
   


# Optional: extend User model by linking to HospitalRole (if your user model doesn't already have a role field)
# If you already have user.role as a CharField, adapt accordingly. This helper field is non-required.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(HospitalRole, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Profile: {self.user} - {self.role}"







































# from django.db import models

# # Just a placeholder so Django creates migrations for this app
# class PermissionPlaceholder(models.Model):
#     class Meta:
#         permissions = [
#             ("can_prescribe_medicine", "Can prescribe medicine"),
#             ("can_view_all_patients", "Can view all patient records"),
#             ("can_update_vitals", "Can update patient vital signs"),
#             ("can_assist_doctor", "Can assist doctor in treatments"),
#             ("can_dispense_medicine", "Can dispense medicine"),
#             ("can_manage_inventory", "Can manage drug inventory"),
#             ("can_process_payment", "Can process pharmacy payments"),
#             ("can_manage_staff", "Can add/remove staff"),
#             ("can_view_reports", "Can view hospital reports"),
            
#             ("can_view_own_record", "Can view own medical record"),
#         ]
#         managed = False  # Django won’t create a table for this
        
        
# class PermissionRole(models.Model):
#     role = models.CharField(max_length=255, null=True, blank=True)
#     code = models.CharField(max_length=255, null=True, blank=True)
#     desc = models.CharField(max_length=255, blank=True, null=True)
    
    
#     def __str__(self):
#         return self.role

# =================================


# from django.db import models
# from django.conf import settings
# from django.contrib import admin
# from django.core.management.base import BaseCommand
# from django.urls import path
# from django.utils import timezone
# import uuid


# # ========== MODELS ==========


# class Permission(models.Model):
# """
# Atomic permission codes used across the hospital.
# """
# id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# code = models.CharField(max_length=120, unique=True)
# description = models.TextField(blank=True)


# def __str__(self):
# return self.code




# class HospitalRole(models.Model):
#     """
#     Roles in the single hospital (Main_Admin, Hospital_Admin, Doctor, Nurse, Pharmacist, Pharmacy_Cashier,
#     Lab Technician, Receptionist, Accountant, Patient)
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)


#     def __str__(self):
#         return self.name




# class RolePermission(models.Model):
#     """
#     Mapping of role -> permission (enabled/disabled)
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     role = models.ForeignKey(HospitalRole, on_delete=models.CASCADE, related_name='role_permissions')
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
#     is_enabled = models.BooleanField(default=True)


#     class Meta:
#     unique_together = (('role', 'permission'),)


#     def __str__(self):
#     return f"{self.role.name} -> {self.permission.code} ({'EN' if self.is_enabled else 'DIS'})"




# # Optional: extend User model by linking to HospitalRole (if your user model doesn't already have a role field)
# # If you already have user.role as a CharField, adapt accordingly. This helper field is non-required.
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     role = models.ForeignKey(HospitalRole, on_delete=models.SET_NULL, null=True, blank=True)


#     def __str__(self):
#     return f"Profile: {self.user} - {self.role}"