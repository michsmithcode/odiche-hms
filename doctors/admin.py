from django.contrib import admin
from .models import DoctorProfile, ValidLicense
# Register your models here.

admin.site.register(DoctorProfile)
admin.site.register(ValidLicense)


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "created_at")
    list_filter = ("specialization",)
    search_fields = (
        "first_name",
        "last_name",
        "specialization",
    )
