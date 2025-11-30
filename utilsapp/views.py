from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model
from django.http import JsonResponse
#from .models import EmailOTP
from accounts.tasks import  send_user_otp_email # send_otp_email
from datetime import datetime
from .generate_email_pyotp import generate_otp




def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        try:
            otp = generate_otp(email)
            send_user_otp_email.delay(email, otp)
            return JsonResponse({'message': 'OTP sent successfully! Check your email.'})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=429)



#==============================NOT YET POSITION===============
#Resend 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .generate_email_pyotp import re_generate_otp


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp_view(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        result = re_generate_otp(email)
        return Response(result, status=status.HTTP_200_OK)

    except ValueError as e:
        message = str(e).lower()
        if "wait" in message:
            return Response({"error": str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        elif "not found" in message:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Unexpected error in resend_otp_view:", e)
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(["POST"])
# @permission_classes([AllowAny])
# def resend_otp_view(request):
#     """
#     Resend OTP to a user’s registered email.
#     """
#     email = request.data.get("email")
#     if not email:
#         return JsonResponse({"error": "Email is required."}, status=400)

#     try:
#         result = re_generate_otp(email)
#         return JsonResponse(result, status=200)

#     except ValueError as e:
#         message = str(e).lower()
#         if "wait" in message:
#             return JsonResponse({"error": str(e)}, status=429)
#         elif "not found" in message:
#             return JsonResponse({"error": str(e)}, status=404)
#         else:
#             return JsonResponse({"error": str(e)}, status=400)

#     except Exception as e:
#         return JsonResponse({"error": "An unexpected error occurred."}, status=500)






# @api_view(["POST"])
# @permission_classes([AllowAny])
# def resend_otp_view(request):
#     email = request.data.get("email")

#     if not email:
#         return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
    
#     #fetch the user
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

#     # Attempt to resend OTP
#     otp = resend_otp(email)
    
#     return Response(
#         {"message": "A new OTP has been sent to your email."},
#         status=status.HTTP_200_OK,
#     )



