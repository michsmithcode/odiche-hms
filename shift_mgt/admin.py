from django.contrib import admin
from .models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "date",
        "start_time",
        "end_time",
        "shift_type",
        "assigned_by",
        "created_at",
    )
    list_filter = (
        "role",
        "shift_type",
        "date",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__surname",
        "user__email",
    )
    readonly_fields = ("created_at", "assigned_by")

    def save_model(self, request, obj, form, change):
        # Auto-assign "assigned_by"
        if not obj.assigned_by:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
