
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from permissions.models import HospitalRole, UserProfile
# Import role-based profile models for all existing roles
from doctors.models import DoctorProfile
from nurses.models import NurseProfile
from patients.models import PatientProfile
from hospitaladmin.models import HospitalAdminProfile
from pharmacycashiers.models import PharmacyCashierProfile
from pharmarcist.models import PharmacistProfile
from mainadmin.models import MainAdminProfile
from accountant.models import AccountantProfile
from receptionists.models import ReceptionistProfile
from lab_technician.models import LabTechnicianProfile


@receiver(post_save, sender=CustomUser)
def create_role_profile(sender, instance, created, **kwargs):
    """
    Assign HospitalRole and auto-create the corresponding profile
    when a new CustomUser is created (including invited users).
    """

    if not created:
        return

    role_name = instance.role  # role stored as string in CustomUser

    # -------------------------
    # 1. ASSIGN USER → HospitalRole
    # -------------------------
    try:
        hospital_role = HospitalRole.objects.get(name__iexact=role_name)
    except HospitalRole.DoesNotExist:
        hospital_role = None  # Role not found (optional: log this)

    # Always create or attach a UserProfile
    UserProfile.objects.update_or_create(
        user=instance,
        defaults={"role": hospital_role}
    )

    # -------------------------
    # 2. AUTO-CREATE PROFILE BASED ON ROLE
    # -------------------------
    match role_name.lower():

        case "doctor":
            DoctorProfile.objects.get_or_create(user=instance)

        case "nurse":
            NurseProfile.objects.get_or_create(user=instance)

        case "patient":
            PatientProfile.objects.get_or_create(user=instance)

        case "pharmacist":
            PharmacistProfile.objects.get_or_create(user=instance)

        case "cashier":
            PharmacyCashierProfile.objects.get_or_create(user=instance)

        case "hospital_admin":
            HospitalAdminProfile.objects.get_or_create(user=instance)

        case "main_admin":
            MainAdminProfile.objects.get_or_create(user=instance)

        case "accountant":
            AccountantProfile.objects.get_or_create(user=instance)

        case "receptionist":
            ReceptionistProfile.objects.get_or_create(user=instance)

        case "labtechnician":
            LabTechnicianProfile.objects.get_or_create(user=instance)

        case _:
            # Unknown role, skip silently
            pass













#========================PREVIOUS VERSION
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser
# from permissions.models import Role, UserRole, HospitalRole

# from doctors.models import Doctor
# from nurses.models import Nurse
# from patients.models import Patient
# from hospitaladmin.models import HospitalAdmin
# from pharmacycashiers.models import PharmacyCashier

# from mainadmin.models import MainAdmin
# from accountants.models import Accountant
# from receptionists.models import Receptionist
# from labtechnicians.models import LabTechnician


# @receiver(post_save, sender=CustomUser)
# def create_role_profile(sender, instance, created, **kwargs):
#     """
#     Automatically assigns role and creates related profile model
#     when a CustomUser is created (including invitations).
#     """

#     if not created:
#         return

#     role_name = instance.role  # stored on CustomUser as string

#     # --- 1. Assign Role + UserRole ---
#     try:
#         role = Role.objects.get(name=role_name)
#         UserRole.objects.create(user=instance, role=role)
#     except Role.DoesNotExist:
#         pass  # You may log this later if needed

#     # --- 2. Auto-create profile based on role ---
#     match role_name:
#         case "doctor":
#             Doctor.objects.get_or_create(user=instance)

#         case "nurse":
#             Nurse.objects.get_or_create(user=instance)

#         case "patient":
#             Patient.objects.get_or_create(user=instance)

#         case "pharmacist":
#             Pharmacist.objects.get_or_create(user=instance)

#         case "cashier":  # FIXED typo
#             PharmacyCashier.objects.get_or_create(user=instance)

#         case "hospital_admin":
#             HospitalAdmin.objects.get_or_create(user=instance)

#         case "main_admin":
#             MainAdmin.objects.get_or_create(user=instance)

#         case "accountant":
#             Accountant.objects.get_or_create(user=instance)

#         case "receptionist":
#             Receptionist.objects.get_or_create(user=instance)

#         case "labtechnician":
#             LabTechnician.objects.get_or_create(user=instance)

#         case _:
#             pass  # Unknown role (optional: log it)



















# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# #from permissions.models import Role, UserRole
# from .models import CustomUser
# from doctors.models import Doctor
# from nurses.models import Nurse
# from patients.models import Patient
# from hospitaladmin.models import HospitalAdmin
# from pharmacycashiers.models import PharmacyCashier
# from pharmarcist.models import Pharmacist
# from mainadmin.models import MainAdmin


# @receiver(post_save, sender=CustomUser)
# def create_role_profile(sender, instance, created, **kwargs):
#     if created:
#         role_name = instance.role  # string stored on CustomUser
    
#         try:
#             role = Role.objects.get(name=role_name)
#             UserRole.objects.create(user=instance, role=role)
#         except Role.DoesNotExist:
#             pass


#         # auto-create profile object for role during invite
#         if role_name == "doctor":
#             Doctor.objects.get_or_create(user=instance)
#         elif role_name == "nurse":
#             Nurse.objects.get_or_create(user=instance)
#         elif role_name == "patient":
#             Patient.objects.get_or_create(user=instance)
#         elif role_name == "pharmacist":
#             Pharmacist.objects.get_or_create(user=instance)
#         elif role_name == "chashier":
#             PharmacyCashier.objects.get_or_create(user=instance)
#         elif role_name == "hospital_admin":
#             HospitalAdmin.objects.get_or_create(user=instance)
#         elif role_name == "main_admin":
#             MainAdmin.objects.get_or_create(user=instance)
#         elif role_name== "accountant":
#                 Accountant.objects.get_or_create(user=instance)
#         elif role_name == "receptionist":
#                 Receptionist.objects.get_or_create(user=instance)
#         elif role_name == "labtechnician":
#                 Labtechnician.objects.get_or_create(user=instance)
     
