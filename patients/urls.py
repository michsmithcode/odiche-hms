from django.urls import path
from . import views


urlpatterns = [
    path("profile/",views.patient_view_profile, name="patient-view-profile"),
    path("register/", views.register_patient, name="create-patient"),
    path("list/", views.list_patients, name="list-patients"),
    path("search_reg_no/",views.search_by_reg_no, name="search-by-reg-no"),
    path("search_folder/", views.search_by_folder, name="search-by-folder"),
    path("search_card/", views.search_patient_by_card, name="search-patient"),
    
    #admin
    path("admin/<int:pk>/detail/", views.admin_patient_detail, name="admin-patient-detail"),
    path("admin/<int:pk>/verify/", views.admin_verify_patient, name="admin-verify-patient"),
    path("dashboard/", views.patient_dashboard, name="patient-dashboard"),
]


#testing methods
#by admin; POST /api/patients/<pk>/verify/
#GET /api/patients/search/?card_no=PT1001
#GET /api/patients/?page=1
#GET /api/receptionist/dashboard/


