from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

#This function is for sending a password reset email to a patien
def send_password_reset_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

    subject = "Password Reset - Hospital Portal"
    message = (
        f"Hello {user.first_name},\n\n"
        f"A hospital account has been created for you.\n"
        f"Please click the link below to set your password:\n\n"
        f"{reset_link}\n\n"
        "If you did not request this, please ignore this email."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return reset_link  # Useful for POSTMAN testing
