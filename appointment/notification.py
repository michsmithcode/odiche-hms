from django.core.mail import send_mail
from django.conf import settings

def send_patient_appointment_notification(patient, doctor, appointment_datetime):
    subject = "Your Appointment Has Been Scheduled"
    message = (
        f"Dear {patient.user.first_name},\n\n"
        f"An appointment has been scheduled for you.\n\n"
        f"Doctor: Dr. {doctor.user.last_name}\n"
        f"Date & Time: {appointment_datetime}\n\n"
        f"Please arrive 10 minutes before your scheduled time.\n\n"
        f"Thank you,\nHospital Team"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.user.email],
        fail_silently=False,
    )
