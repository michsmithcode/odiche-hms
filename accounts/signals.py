
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from permissions.models import HospitalRole, UserProfile

# Import role-based profile models for all existing roles
from doctors.models import DoctorProfile
from nurses.models import NurseProfile
#from patients.models import PatientProfile
from hospitaladmin.models import HospitalAdminProfile
from pharmacycashiers.models import PharmacyCashierProfile
from pharmarcist.models import PharmacistProfile
#from mainadmin.models import MainAdminProfile
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

    # if role_name == "patient":
    
    # Assing user's HospitalRole
    
    try:
        hospital_role = HospitalRole.objects.get(name__iexact=role_name)
    except HospitalRole.DoesNotExist:
        hospital_role = None  # Role not found (optional: log this)

    # Always create or attach a UserProfile
    UserProfile.objects.update_or_create(
        user=instance,
        defaults={"role": hospital_role}
    )

    
    # Auto_create profile based on user role using match Case Method
    
    match role_name.lower():

        case "doctor":
            DoctorProfile.objects.get_or_create(user=instance)

        case "nurse":
            NurseProfile.objects.get_or_create(user=instance)

        case "pharmacist":
            PharmacistProfile.objects.get_or_create(user=instance)

        case "cashier":
            PharmacyCashierProfile.objects.get_or_create(user=instance)

        case "hospital_admin":
            HospitalAdminProfile.objects.get_or_create(user=instance)

        # case "main_admin":
        #     MainAdminProfile.objects.get_or_create(user=instance)

        case "accountant":
            AccountantProfile.objects.get_or_create(user=instance)

        case "receptionist":
            ReceptionistProfile.objects.get_or_create(user=instance)

        case "labtechnician":
            LabTechnicianProfile.objects.get_or_create(user=instance)

        case _:
            # Unknown role, skip silently
            pass
        
        
    #patient account creation already handled by the receptionist
        # case "patient":
        #     PatientProfile.objects.get_or_create(user=instance)
