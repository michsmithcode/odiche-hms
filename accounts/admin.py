
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Use email instead of username
    list_display = ("id", "email", "first_name", "last_name", "is_staff", "is_active",  'is_otp_verified')
    list_filter = ("is_staff", "is_active",  'is_otp_verified')

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", 'is_otp_verified')}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff", 'is_otp_verified'),
        }),
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)



#==========================Old==================

# from django.contrib import admin
# #from .models import CustomUser
# # Register your models here.


# #admin.site.register(CustomUser)

# #oR 
# # from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

# User = get_user_model()

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'is_active', 'is_staff', 'is_otp_verified')
#     search_fields = ('email')
#     list_filter = ('is_active', 'is_staff', 'is_otp_verified')
