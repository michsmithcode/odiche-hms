from django.urls import path
from . import views


from django.urls import path
from .views import (
    create_patient,
    admin_patient_detail,
    search_patient_by_card,
    list_patients,
    receptionist_dashboard,
    admin_verify_patient,
)

urlpatterns = [
    path("create/", create_patient, name="create-patient"),
    path("", list_patients, name="list-patients"),
    path("search/", search_patient_by_card, name="search-patient"),
    path("admin/","<int:pk>/", admin_patient_detail, name="admin-patient-detail"),
    path("admin/","<int:pk>/verify/", admin_verify_patient, name="admin-verify-patient"),
    path("dashboard/", receptionist_dashboard, name="receptionist-dashboard"),
]

# urlpatterns = [
#     # Receptionist
#     path("register/", views.register_patient, name="register-patient"),

#     # Patient
#     path("profile/", views.patient_self_view, name="patient-self"),

#     # Admin
#     path("admin/view_all/", views.admin_patient_list, name="admin-patient-list"),
#     path("admin/<int:pk>/", views.admin_patient_detail, name="admin-patient-detail"),
# ]


#by admin; POST /api/patients/<pk>/verify/
#GET /api/patients/search/?card_no=PT1001
#GET /api/patients/?page=1
#GET /api/receptionist/dashboard/


