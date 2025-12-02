from django.contrib import admin
from .models import DoctorProfile, ValidLicense
# Register your models here.

admin.site.register(DoctorProfile)
admin.site.register(ValidLicense)