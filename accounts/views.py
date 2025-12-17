from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .serializers import UserInviteSerializer
from django.contrib import messages
#from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

#===========================
from django.contrib.auth import authenticate
from .tasks import send_user_otp_email
from utilsapp.generate_email_pyotp import generate_otp, verify_otp
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


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
        send_user_otp_email.delay_on_commit(email=user.email,first_name=user.first_name, otp_code=otp,time=2400)
        
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

