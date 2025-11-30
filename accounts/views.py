from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .serializers import UserInviteSerializer
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

#===========================
from django.contrib.auth import authenticate
from .tasks import send_user_otp_email
from utilsapp.generate_email_pyotp import generate_otp, verify_otp
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()



#from rest_framework.response import Response
#from rest_framework import status
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.tokens import RefreshToken


"""
 "message": "Login successful.",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzMDEyMjMzLCJpYXQiOjE3NjMwMTEzMzMsImp0aSI6IjgwYTA4ZDljNzgzMDQxZjJhOGNlODE1ZjI2MTM2OThjIiwidXNlcl9pZCI6IjJkNDdlNzBmLWVmZWEtNGQxNC05NGVlLTNmZjdkNmQwYTY2ZSJ9.C8XCf2GtHm_ykDD2zCau0LWpMMPvZ4i95BI-Bl_a5_0",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MzE4NDEzMywiaWF0IjoxNzYzMDExMzMzLCJqdGkiOiI2Y2RkOTBlMDJmMTY0YThmYmVjYmQ5NjRkNWIxOWQwYyIsInVzZXJfaWQiOiIyZDQ3ZTcwZi1lZmVhLTRkMTQtOTRlZS0zZmY3ZDZkMGE2NmUifQ.wRbAmILpkeIvm5IokUVCx2B3oVbJSx7t4nIChAnSeBc",
    "user": {
        "email": "exampledoctor@gmail.com",
        "role": "doctor",
        "is_active": true
    }
}
"""


#POSTMAN REG DETAILS
"""
   "email": "example@gmail.com",
  "first_name": "udoka",
  "last_name": "ubong",
  "role": "doctor",
  "state": "Abia"
"""


"""
  "email": "exampledoctor@gmail.com", 
  "first_name": "dogman",
  "last_name": "dogman",
  "role": "doctor",
  "state": "Abia"
  verify code:"511680"

{
    "Successful registration "
  "email": "exampledoctor@gmail.com",
  "first_name": "dog",
  "last_name": "dog",
  "role": "doctor",
  "state": "Akwa Ibom",
  "password": "12345"
}

USE THIS ACCOUNT
{
  "email": "test@gmail.com",
  "first_name": "test",
  "last_name": "test1",
  "role": "doctor",
  "state": "Akwa Ibom",
  "password": "12345"
  {
    "message": "Login successful.",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MDM2MzM0LCJpYXQiOjE3NjQwMzU0MzQsImp0aSI6ImIzM2QxN2Q0NWM2MjRmYTRhNDhlMjRiZTRlMzE3OGJiIiwidXNlcl9pZCI6IjNhMjIwNWQ5LTA5YjAtNDQ5Mi04NTJjLWZmZDk1M2NmNTk0NiJ9.ta2HtQcXbWPlLO4qzGfuBXbxdr__pjPt7NhLLEHw9O8",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDIwODIzNCwiaWF0IjoxNzY0MDM1NDM0LCJqdGkiOiIzNGRhYzhhY2M2NjI0MzUxOWRjZWI5NzUzMDY4YjYxZiIsInVzZXJfaWQiOiIzYTIyMDVkOS0wOWIwLTQ0OTItODUyYy1mZmQ5NTNjZjU5NDYifQ.3ncHXPSBsM0qNpm_ABfGOWY3MeKQVF9gluUe7CfhrTs",
    "user": {
        "email": "test@gmail.com",
        "role": "Doctor",
        "is_active": true
    }
    { #New ACCESS token
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MTU2NjcyLCJpYXQiOjE3NjQxNTU3NzIsImp0aSI6IjJjYjRjNmVjMGYzZTQzNzRiZTRhNTg0MWRjZmZhMWQwIiwidXNlcl9pZCI6IjNhMjIwNWQ5LTA5YjAtNDQ5Mi04NTJjLWZmZDk1M2NmNTk0NiJ9.rtYW6BE1fSqmc6iLBgU7VNSqJlNfzp3-iVAoVDQGvSs",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDMyODU3MiwiaWF0IjoxNzY0MTU1NzcyLCJqdGkiOiIxNTFkNjUzOTVhMzM0MjliOTRkZDI3OWE5OGEwYTAwZSIsInVzZXJfaWQiOiIzYTIyMDVkOS0wOWIwLTQ0OTItODUyYy1mZmQ5NTNjZjU5NDYifQ.pCjIGjH0W01LcSFeqgYS0QkHwEQ1G9PFC7X9xhENucs"
}
#New 
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MTYyMTgwLCJpYXQiOjE3NjQxNTg1ODAsImp0aSI6Ijg2MTNmMzcxMzc5MjRmM2M4MzQ2YzMyMTdjYmJlMjUwIiwidXNlcl9pZCI6IjNhMjIwNWQ5LTA5YjAtNDQ5Mi04NTJjLWZmZDk1M2NmNTk0NiJ9.l2JvE7JxEgLPlCkE_BNHSw6BjbZTNHvNmmPwK16CFSI",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDMzMTM4MCwiaWF0IjoxNzY0MTU4NTgwLCJqdGkiOiIzNTJiYmIxMTYxZTk0YzBiODRkZjM0YzMwNzhiOTRmNiIsInVzZXJfaWQiOiIzYTIyMDVkOS0wOWIwLTQ0OTItODUyYy1mZmQ5NTNjZjU5NDYifQ.UsGqgBBE84Swx6SeMzrFV2J52b3cyUkDdeNtRuY1qL8"
}
}
}
"""


# # Setting roles for each user once creating an account
VALID_ROLES = ["doctor", "nurse", "pharmacist", "pharmacy_cashier", "receptionist", "main_admin", "hospital_admin", "accountant", "lab_technician", "patient"]


@permission_classes([permissions.IsAdminUser])  # Only admins can invite
@api_view(["POST"])
@csrf_exempt
def invite_user(request):
    role = request.data.get("role")
    email = request.data.get("email")

    if role not in VALID_ROLES:
        return Response(
            {"error": f"Invalid role. Choose from: {', '.join(VALID_ROLES)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)


    data = request.data.copy()
    data["role"] = role
    data["password"] = None  #to reset password, change later with OTP/email link
    


    serializer = UserInviteSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save(is_active=False)  # create and make the user inactive account first
        

        #Assign the role to the user's Profile (This is very IMPORTANT)
        from permissions.models import HospitalRole, UserProfile
        
        role_obj = HospitalRole.objects.get(name__iexact=role)
        # Create or update UserProfile
        UserProfile.objects.update_or_create(user=user, role=role_obj)
        
        # Generate OTP and send verification email asynchronously
       
        otp = generate_otp(user.email)
        send_user_otp_email.delay_on_commit(email=user.email,first_name=user.first_name, otp_code=otp,time=1200)
        
        return Response(
            {
                "message": f"{role_obj.name} {user.email} invited successfully" #{user.role.capitalize()} {user.email} invited successfully
               "OTP has been sent to your Email. Kindly check your Email to activate your account",
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp_code(request):
    """
    Verify the OTP sent to the user's email.
    """
    email = request.data.get("email")
    otp_code = request.data.get("otp_code")
    
     # Debug prints — ADD THESE
    print("=== VERIFY OTP DEBUG ===")
    print("Email:", email)
    print("OTP Code:", otp_code)
    # print("Cache Data:", cache.get(f"otp_{email}"))
    # print("=========================")


    if not email or not otp_code:
        return Response(
            {"error": "Email and OTP code are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "No account found with this email."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Verify OTP Code
    if verify_otp(email, otp_code):
        user.is_otp_verified = True
        user.save()
        print(f"{user.email} verified:", user.is_otp_verified)
        
        return Response(
            {"message": "OTP verified successfully. Proceed to activate your account"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "Invalid or expired OTP."},
            status=status.HTTP_400_BAD_REQUEST,
        )

 
#activate the user and create password
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def activate_invite(request):
    """
    Activate the user's account after OTP verification
    by setting a new password.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )
        
        
#check if user is already activated

    if user.is_active:
        return Response(
            {"message": "Account already activated."},
            status=status.HTTP_400_BAD_REQUEST,
        )

# This ensures OTP is verified first
    if not getattr(user, "is_otp_verified", False):
        return Response(
            {"error": "Please verify your OTP before activating your account."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Set password and activate account
    user.set_password(password)
    user.is_active = True
    user.save()

    return Response(
        {"message": "Account activated successfully. You can now log in."},
        status=status.HTTP_200_OK,
    )



#account loging and permission token obtain

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

3
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """
    User login after activation (JWT-based authentication)
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response(
            {"error": "Invalid credentials or inactive account."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return Response(
            {"error": "Please activate your account first."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                #This uses the user profile crated at the permission models 
                "role": user.profile.role.name if hasattr(user, "profile") and user.profile.role else None,
                #"role": getattr(user, "role", None),
                "is_active": user.is_active,
            },
        },
        status=status.HTTP_200_OK,
    )








#----------------------NOT USED------------------------------
#using AcessToken for account actiavation
#@api_view(["POST"])
#@permission_classes([AllowAny])
# def activate_invite(request):
#     token = request.data.get("token")
#     password = request.data.get("password")

#     if not token or not password:
#         return Response({"error": "Token and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         access = AccessToken(token)
#         user_id = access["user_id"]
#         user = User.objects.get(id=user_id)

#         if user.is_active:
#             return Response({"message": "User already activated"}, status=status.HTTP_400_BAD_REQUEST)

#         # activate account and set password
#         user.set_password(password)
#         user.is_active = True
#         user.save()

#         return Response({"message": "Account activated successfully. You can now log in."}, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({"error": f"Invalid or expired token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

#user....add(element)
#email: janedoe@example.com
#password: 1234

#refresh and access token
"""
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTkxODYwNywiaWF0IjoxNzU5ODMyMjA3LCJqdGkiOiIwMWM5ZWRmMDA1NGI0OTc2OWJhNjk4MjhmYjZmMTJkNyIsInVzZXJfaWQiOiJiYWQxOTQwOS1mODIzLTQ3YWEtYTdhZC04ZWE2ZTZlZDk4YTEifQ.2K190y5ntqr7vN-SMArAeHACWMNOKvsbE_Br-B8HGBc",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5ODMzMTA3LCJpYXQiOjE3NTk4MzIyMDcsImp0aSI6ImRmNTg3YjlmMmYwYTQxMTViYTdhNWMzNGNjODhiY2YzIiwidXNlcl9pZCI6ImJhZDE5NDA5LWY4MjMtNDdhYS1hN2FkLThlYTZlNmVkOThhMSJ9.rV5Bin9jTzKmnw9NdDDRIBP0EtH_EbHqM2zoWZph7EI"
}"""

#activation link
#http://127.0.0.1:8000/api/accounts/activate/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5ODIxODIwLCJpYXQiOjE3NTk4MjA5MjAsImp0aSI6IjcyNjBmNzg4MDc1YTQ4NjBiZDcxZjk2NmYzZWZkZGMyIiwidXNlcl9pZCI6IjUyNTEzMTRiLTgyMjctNGI3OC04ZWMxLWMwMWUzNWYzYjQwYyJ9.P8wHfmB63ELg_h9Bnf15LnpwXBi5WhkpZdmoXlAfuv8

# @api_view(['POST'])
# @permission_classes([AllowAny])  # anyone can attempt login
# def custom_token_obtain_pair(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     user = authenticate(request, email=email, password=password)

#     if user is not None:
#         refresh = RefreshToken.for_user(user)

#         # Add custom claims (role, username, etc.)
#         refresh['role'] = user.role
#         refresh['email'] = user.email

#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'role': user.role,
#             'email': user.email,
#         })
#     else:
#         return Response(
#             {"detail": "Invalid credentials"},
#             status=status.HTTP_401_UNAUTHORIZED
#         )



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def custom_token_refresh(request):
#     refresh_token = request.data.get("refresh")

#     try:
#         refresh = RefreshToken(refresh_token)
#         new_access = refresh.access_token
#         return Response({
#             "access": str(new_access)
#         })
#     except Exception:
#         return Response(
#             {"detail": "Invalid refresh token"},
#             status=status.HTTP_401_UNAUTHORIZED
#         )








# @api_view(["POST"])
# #@permission_classes([permissions.IsAdminUser])  # Only Admins can invite
# def user_invite(request):
#     serializer = UserInviteSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         return Response(
#             {"message": f"{user.role.capitalize()} {user.email} invited successfully"},
#             status=status.HTTP_201_CREATED
#         )

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# #setting roles
# VALID_ROLES = ["doctor", "nurse", "pharmacist", "pharmacy_cashier", "hospital_admin", "patient"]

# @api_view(["POST"])
# #@permission_classes([permissions.IsAdminUser])  # Only admins can invite
# def invite_user(request):
#     role = request.data.get("role")
#     email = request.data.get("email")
#     first_name = request.data.get("first_name", "")
#     surname = request.data.get("surname", "")
#     last_name = request.data.get("last_name", "")

    # # Validate role as indicated in the role lists
    # if role not in VALID_ROLES:
    #     return Response(
    #         {"error": f"Invalid role. Choose from: {', '.join(VALID_ROLES)}"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # # Check valid email and exitence
    # if not email:
    #     return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    # if User.objects.filter(email=email).exists():
    #     return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    # serializer = UserInviteSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    

    # Creating a user
    # user = User.objects.create_user(
    #     email=email,
    #     first_name=first_name,
    #     surname=surname,
    #     last_name=last_name,
    #     role=role,
    #     password="default12345" 
    # )

    # return Response(
    #     {"message": f"{role.capitalize()} {user.email} invited successfully"},
    #     status=status.HTTP_201_CREATED
    # )


#class BasedViews
# from rest_framework import generics, permissions
# from django.contrib.auth import get_user_model
# from .serializers import UserInviteSerializer

# class UserInviteView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserInviteSerializer
#     permission_classes = [permissions.AllowAny]  # Change later to AdminOnly

