from django.contrib import admin
from .models import Admission, Treatment
# Register your models here.

admin.site.register(Admission)
admin.site.register(Treatment)


# from django.contrib import admin
# from .models import Treatment


#@admin.register(Treatment)
# class TreatmentAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "admission",
#         "doctor",
#         "procedure_name",
#         "date",
#     )

#     search_fields = (
#         "procedure_name",
#         "medication_prescribed",
#         "admission__patient__reg_no",
#     )

#     list_filter = ("date",)

#     fieldsets = (
#         ("Patient & Admission", {
#             "fields": ("admission", "doctor", "date")
#         }),
#         ("Treatment Details", {
#             "fields": (
#                 "procedure_name",
#                 "medication_prescribed",
#                 "description",
#                 "notes",
#             )
#         }),
#     )

#     readonly_fields = ("date",)
