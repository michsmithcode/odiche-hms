from django.contrib import admin
from .models import PatientProfile

admin.site.register(PatientProfile)


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = [
        "first_name", "last_name", "reg_no", "file_folder_no",
        "card_no", "gender", "state", "created_at", "is_verified"
    ]

    search_fields = [
        "first_name", "last_name", "reg_no", "file_folder_no", "card_no"
    ]

    list_filter = [
        "gender", "state", "created_at", "is_verified"
    ]

    list_per_page = 25
