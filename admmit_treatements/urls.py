from django.urls import path
from . import views

urlpatterns = [
    # Admissions
    path("admit/", views.admit_patient, name="admit-patient"),
    path("list/", views.list_patient_admissions, name="list_patient-admission"),
    path("detail/<int:pk>/", views.admission_detail, name="admission-detail"),
    path("update/<int:pk>/update/", views.update_admission, name="update-admission"),
    path("discharge/<int:admission_id>/", views.discharge_patient, name="discharge-patient"),

    # Treatments
    path("treatment/add/", views.administer_treatment, name="administer-treatment"),
    path("treatment/list/<int:admission_id>/", views.list_treatments, name="list-treatment"),
    path("treatment/update/<int:pk>/update/", views.update_treatment, name="update-treatment"),
]
