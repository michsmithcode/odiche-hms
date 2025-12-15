# from twilio.rest import Client
# from django.conf import settings

# def send_sms_notification(phone_number, message):
#     client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH)

#     client.messages.create(
#         body=message,
#         from_=settings.TWILIO_NUMBER,
#         to=phone_number
#     )
