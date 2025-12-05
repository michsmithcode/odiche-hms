# from django.core.mail import send_mail

# def send_appointment_notification(appointment):
#     send_mail(
#         subject="New Appointment Scheduled",
#         message=f"You have a new appointment on {appointment.appointment_date}",
#         from_email="hospital@example.com",
#         recipient_list=[appointment.doctor.user.email, appointment.nurse.user.email, appointment.patient.user.email],
#         fail_silently=True,
#     )
