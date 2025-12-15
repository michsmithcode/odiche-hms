from datetime import time

def get_available_doctor_for_datetime(appointment_datetime):
    """Find a doctor whose shift covers the appointment date/time."""
    from .models import Shift  # avoid circular import

    appointment_time = appointment_datetime.time()

    # Find all shifts where the appointment_time falls within the shift time
    matching_shifts = Shift.objects.filter(
        start_time__lte=appointment_time,
        end_time__gte=appointment_time
    ).select_related("assigned_doctor")

    if not matching_shifts.exists():
        return None

    # Prefer verified nurses
    matching_shifts = [
        s for s in matching_shifts if s.assigned_doctor and s.assigned_doctor.is_verified
    ]

    if not matching_shifts:
        return None

    # If multiple doctors available → pick the least busy doctor
    matching_shifts.sort(key=lambda s: s.assigned_doctor.appointments.count())

    return matching_shifts[0].assigned_doctor
