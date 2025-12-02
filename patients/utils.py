from .models import PatientProfile
import uuid


def generate_reg_no():
    """
    Generates something like: REG-2025-00123
    """
    from django.utils import timezone
    year = timezone.now().year
    random_code = str(uuid.uuid4().int)[:5]
    return f"REG-{year}-{random_code}"





def generate_card_number():
    last_patient = PatientProfile.objects.order_by("id").last()
    if not last_patient:
        return "PT0001"

    last_card = int(last_patient.card_no.replace("PT", ""))
    new_card = last_card + 1
    return f"PT{new_card:04d}"



def generate_file_folder_no():
    """
    Generates folder number: FOLDER-000123
    """
    return f"FOLDER-{str(uuid.uuid4().int)[:6]}"



# def generate_folder_no():
#     last_patient = PatientProfile.objects.order_by("id").last()
#     next_id = (last_patient.id + 1) if last_patient else 1
#     return f"HF-{str(next_id).zfill(6)}"

