from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
import uuid


ROLE_CHOICES = [
    ("main_admin", "MAIN ADMIN"),
    ("hospital_admin", "HOSPITAL ADMIN"),
    ("doctor", "DOCTOR"),
    ("nurse", "NURSE"),
    ("accountant", "ACCOUNTANT"),
    ("pharmacist", "PHARMACIST"),
    ("pharmacy_cashier", "PHARMACY CASHIER"),
    ("lab_technician", "LAB TECHNICIAN"),
    ("receptionist", "RECEPTIONIST"),
    ("patient", "PATIENT")
    
    
    ]



GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female")
    ]



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with email and password.
        """
        if not email:
            raise ValueError("Email Required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None, **extra_fields):
        """
        Create and return a superuser with admin rights.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password=password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    email= models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    profile_photo = models.ImageField(upload_to="profile/", blank=True,  null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
 
 
 
 