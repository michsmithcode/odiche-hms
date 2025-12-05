# from doctors.models import DoctorProfile
# from shifts.models import Shift
# from django.utils import timezone

# def assign_doctor_by_specialization(specialization):
#     today = timezone.now().date()

#     doctor = (
#         DoctorProfile.objects.filter(
#             specialization=specialization,
#             user__shift__start_date__lte=today,
#             user__shift__end_date__gte=today
#         )
#         .order_by("?")
#         .first()
#     )

#     return doctor
