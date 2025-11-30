"""
ADMIN token;
{
    "message": "Login successful.",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MjE1NzAxLCJpYXQiOjE3NjQyMTIxMDEsImp0aSI6ImI2NzRiOWI2NmU5ZTQzYzlhYTEyZTAzNjNiNGEzMWNjIiwidXNlcl9pZCI6ImFlOGFjMjk4LTQ4OTEtNDBmYy1hZDZiLTM3MzkzZjlkMzQ1ZiJ9.EwGAFlEYUr3-h4a7lTAuvDQyhim7waXndzmw7-Tl5ak",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDM4NDkwMSwiaWF0IjoxNzY0MjEyMTAxLCJqdGkiOiIyMzg2OGMzZjU2OTA0ZWM4YWM4ZGM3NmZlNzY5Zjg0MiIsInVzZXJfaWQiOiJhZThhYzI5OC00ODkxLTQwZmMtYWQ2Yi0zNzM5M2Y5ZDM0NWYifQ.q2_gB0BW_aPycB69LGprKhUBjZKJij84qJFNVmcvUpQ"

"""


"""
New toke

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MzM5NTEwLCJpYXQiOjE3NjQzMzU5MTAsImp0aSI6ImM3ZmNiZjRjZjY2NTQ3OGE5M2UxMmY0MzdlYjZiODhjIiwidXNlcl9pZCI6ImFlOGFjMjk4LTQ4OTEtNDBmYy1hZDZiLTM3MzkzZjlkMzQ1ZiJ9.km1T3g3_mXDyrByORkt8RjcZw9SfdYLNf3S0AQ3ga3c",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDUwODcxMCwiaWF0IjoxNzY0MzM1OTEwLCJqdGkiOiJjYzY3MzA2YmE5NTE0MDgzOTk3MjliZGU0ZDg1MDEzNyIsInVzZXJfaWQiOiJhZThhYzI5OC00ODkxLTQwZmMtYWQ2Yi0zNzM5M2Y5ZDM0NWYifQ.wGIR9hkrLbt1jSFxv_NEYDJyPTuZb5P6mXXBgmeL7zg"
}
"""

"""
29/11
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0Mzk2MDM0LCJpYXQiOjE3NjQzOTI0MzQsImp0aSI6IjgzYzk2MzdiNTBkYTQ4NTJiNGYzMTEyMGQ1ZWJlOGY4IiwidXNlcl9pZCI6ImFlOGFjMjk4LTQ4OTEtNDBmYy1hZDZiLTM3MzkzZjlkMzQ1ZiJ9.ki8RETS0Fmy6Nw97HoBmTeWpB_rOnrUaD2U6L-_RmvM",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDU2NTIzNCwiaWF0IjoxNzY0MzkyNDM0LCJqdGkiOiIzM2Y0ZjI4NWM5ZWE0YTcxYWQxM2QyNTE5MmZiYWJhMiIsInVzZXJfaWQiOiJhZThhYzI5OC00ODkxLTQwZmMtYWQ2Yi0zNzM5M2Y5ZDM0NWYifQ.00tqGBO7ZLiu0QE8qoh_Q_ptKd4LuM4s6rETfEti7wg"
}
"""







# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth import get_user_model
# from .serializers import UserInviteSerializer
# from django.contrib import messages
# #from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# #from rest_framework.response import Response
# #from rest_framework import status
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate

# from .tasks import send_user_otp_email
# from utilsapp.generate_email_pyotp import generate_otp

# User = get_user_model()




# # Setting roles for each user once creating an account
# VALID_ROLES = ["doctor", "nurse", "pharmacist", "pharmacy_cashier", "hospital_admin", "patient"]

# #@api_view(["POST"])
# #@permission_classes([permissions.IsAdminUser])  # Only admins can invite
# def invite_user(request):
#     role = request.data.get("role")
#     email = request.data.get("email")

#     if role not in VALID_ROLES:
#         return Response(
#             {"error": f"Invalid role. Choose from: {', '.join(VALID_ROLES)}"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

    
#     if not email:
#         return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

#     if User.objects.filter(email=email).exists():
#         return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)


#     data = request.data.copy()
#     data["role"] = role
#     data["password"] = None  # temporary password, change later with OTP/email link
    
    
#     serializer = UserInviteSerializer(data=data)
#     if serializer.is_valid():
#         user = serializer.save(is_active=False)  # create and make the user inactive account first

#         # --- Generate short-lived token ---
    
#         #token for longer period
#         refresh = RefreshToken.for_user(user)
#         invite_token = str(refresh.access_token)
#         #token for short period
#         invite_token = AccessToken.for_user(user)
#         invite_token.set_exp(lifetime=timedelta(minutes=15))

#         #--- Build activation link for Postman testing ---
#         activation_link = f"http://127.0.0.1:8000/api/accounts/activate/?token={str(invite_token)}"

#         print(f"Activation link for {email}: {activation_link}")
        

#         otp = generate_otp(user.email)
      
#         return Response(
#             {
#                 "message": f"{user.role.capitalize()} {user.email} invited successfully",
#                 #"activation_link": activation_link
#             },
#             status=status.HTTP_201_CREATED
#         )

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
# #activate the user and create password

# #@api_view(["POST"])
# #@permission_classes([AllowAny])
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

