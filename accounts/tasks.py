from celery import shared_task
from utilsapp.email import TaskWithOnCommit,EmailSender
import logging 


@shared_task
def send_user_otp_email(email, first_name, otp_code,time): 
    email_sender_obj = EmailSender("You're Invited to Join Our Pharmacy on PharmaApp")
    try:
        email_sender_obj.send_otp_email(email, first_name, otp_code,time)
        return f" Email Sent successfully to {email}"
    except Exception as exc:
        return f"Failed to send email to {email}. Exception occured."
          
send_user_otp_email = TaskWithOnCommit(send_user_otp_email)






#==========================OLD not used=======================
# @shared_task
# def send_user_otp_email(email, first_name, otp_code, time):
#     email_sender_obj = EmailSender("You're Invited to Join Our Pharmacy on PharmaApp")
#     try:
#         email_sender_obj.send_otp_email(email, first_name, otp_code, time)
#         return f"Email sent successfully to {email}"
#     except Exception as exc:
#         import traceback
#         error_message = f" Failed to send email to {email}. Exception: {exc}\n{traceback.format_exc()}"
#         print(error_message)
#         return error_message