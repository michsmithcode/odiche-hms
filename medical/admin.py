from django.contrib import admin
from . models import MedicalHistory, PatientVisit, PatientVital
# Register your models here.

admin.site.register(MedicalHistory)
admin.site.register(PatientVisit)
admin.site.register(PatientVital)