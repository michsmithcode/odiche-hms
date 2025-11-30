import pyotp
from django.core.cache import cache
from datetime import datetime, timedelta

def generate_otp(email):
    """
    Generate OTP using PyOTP and store it temporarily in Redis.
    """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=1200)  # expires in 10 min #(To be change later  to 300, after development)
    otp = totp.now()

    #This stores both secret and OTPKEY in Redis memory
    cache_key = f"otp_{email}"
    #test cashe key
    print("Cache Data:", cache.get(f"otp_{email}"))
    print("=========================")

    cache.set(cache_key, {'secret': secret, 'otp': otp}, timeout=1200)  # 10 mins(will be changed later to300se after development)
    return otp




#Method1
def verify_otp(email, otp):
    """
    Verify OTP using the secret stored in Redis.
    """
    cache_key = f"otp_{email}"
    
    data = cache.get(cache_key)
    if not data:
        return False  # expired or not found

    totp = pyotp.TOTP(data['secret'], interval=1200)#(To be change later to 300sec after development)
    if totp.verify(otp):
        cache.delete(cache_key)  # remove after successful verification
        return True
    return False






#===========updated version for resending of OTP===========

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.tasks import send_user_otp_email

User = get_user_model()


def re_generate_otp(email: str) -> str:
    """
    Generates a new OTP, caches it, and sends it to the user via Celery.
    Raises ValueError if OTP was sent too recently or user not found.
    """
    
    cache_key = f"otp_{email}"

    # Prevent frequent OTP requests
    if cache.get(cache_key):
        raise ValueError("Please wait before requesting another OTP.")

    # Validate user
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValueError("User not found.")

    # Generate a new OTP
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=settings.OTP_TTL_SECONDS)
    otp_code = totp.now()

    # Save OTP to cache
    cache.set(cache_key, {'secret': secret, 'otp': otp_code}, timeout=settings.OTP_TTL_SECONDS)


     # # Calculate expiry time for the email
    expiry_time = (datetime.now() + timedelta(seconds=settings.OTP_TTL_SECONDS)).strftime("%I:%M %p")

     # Send OTP email (using Celery + on_commit wrapper)
    #print(f"Sending OTP to {email}: {otp_code}")
    send_user_otp_email.delay(email, user.first_name or "", otp_code, settings.HUMAN_TTL)

    return {
        "otp": otp_code,            # Optional: for debugging only (don’t expose in production)
        "expires_at": expiry_time,
        "valid_for": settings.HUMAN_TTL,
    }



# from django.core.cache import cache
# from django.contrib.auth import get_user_model
# from accounts.tasks import send_user_otp_email
# from django.conf import settings #  import constants from settings

# User = get_user_model()



# def resend_otp(email):
#     cache_key = f"otp_{email}"

#     # Prevent frequent resends
#     existing = cache.get(cache_key)
#     if existing:
#         raise ValueError("Please wait before requesting another OTP")

#     # Generate new OTP
#     secret = pyotp.random_base32()
#     totp = pyotp.TOTP(secret, interval=settings.OTP_TTL_SECONDS)
#     otp_code = totp.now()
#     #will be removed after testing
#     print(otp_code)

    # # Save OTP and secret to cache
    # cache.set(cache_key, {'secret': secret, 'otp': otp_code}, timeout=settings.OTP_TTL_SECONDS)

    # # Fetch user

    # # Calculate expiry time for the email
    # expiry_time = (datetime.now() + timedelta(seconds=settings.OTP_TTL_SECONDS)).strftime("%I:%M %p")

    # # Send OTP email (using Celery + on_commit wrapper)
    # send_user_otp_email.delay_on_commit(email, user.first_name, otp_code, settings.HUMAN_TTL)
    
#     # send this 
#     return {
#         "message": "OTP resent successfully.",
#         "expires_at": expiry_time,
#         "valid_for": settings.HUMAN_TTL
#     }
    
    
#OR Simply use this
    # return {"message": f"OTP resent successfully. Valid for {settings.HUMAN_TTL}."}



#RESeBD

# import pyotp
# from django.core.cache import cache
# from django.core.mail import send_mail
# from django.conf import settings

# def resend_otp(email):
#     cache_key = f"otp_{email}"

#     # Check if an OTP already exists and hasn't expired
#     existing = cache.get(cache_key)
#     if existing:
#         return None  # Signal that resend is too soon

#     # Generate new secret and OTP
#     secret = pyotp.random_base32()
#     totp = pyotp.TOTP(secret, interval=1200)  # 20 minutes
#     otp = totp.now()

#     # Save new OTP to cache
#     cache.set(cache_key, {"secret": secret, "otp": otp}, timeout=1200)

#     # Send OTP to email
#     send_mail(
#         subject="Your new OTP Code",
#         message=f"Your new OTP code is: {otp}. It will expire in 20 minutes.",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[email],
#     )

#     return otp


# #resending OTP
# def resend_otp(email):
#     cache_key = f"otp_{email}"

#     # Check if user recently requested OTP
#     existing = cache.get(cache_key)
#     if existing:
#         raise ValueError("Please wait before requesting another OTP")

#     secret = pyotp.random_base32()
#     totp = pyotp.TOTP(secret, interval=1200)#(To be change later after development)
#     otp = totp.now()

#     cache.set(cache_key, {'secret': secret, 'otp': otp}, timeout=1200)#(To be change later after development)
#     return otp




