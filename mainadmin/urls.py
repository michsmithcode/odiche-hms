from django.urls import path
from . import views



# urlpatterns = [
#     # Doctor
#     path("doctors/", views.admin_list_doctors, name="admin_list_doctors"),
#     path("doctors/<int:doctor_id>/", views.admin_doctor_detail, name="admin_doctor_detail"),

#     # Nurse
#     path("nurses/", views.admin_list_nurses, name="admin_list_nurses"),
#     path("nurses/<int:nurse_id>/", views.admin_nurse_detail, name="admin_nurse_detail"),

#     # Pharmacist
#     path("pharmacists/", views.admin_list_pharmacists, name="admin_list_pharmacists"),
#     path("pharmacists/<int:pharmacist_id>/", views.admin_pharmacist_detail, name="admin_pharmacist_detail"),

#     # Cashier
#     path("cashiers/", views.admin_list_cashiers, name="admin_list_cashiers"),
#     path("cashiers/<int:cashier_id>/", views.admin_cashier_detail, name="admin_cashier_detail"),

#     # Patient
#     path("patients/", views.admin_list_patients, name="admin_list_patients"),
#     path("patients/<int:patient_id>/", views.admin_patient_detail, name="admin_patient_detail"),

  #  Dashboard overview
    #path("dashboard/", views.admin_dashboard_overview, name="admin_dashboard_overview"),
# ]



# urlpatterns = [
#     path("doctors/", views.admin_list_doctors, name="admin_list_doctors"),
#     path("doctors/<int:doctor_id>/", views.admin_get_doctor, name="admin_get_doctor"),
#     path("doctors/<int:doctor_id>/update/", views.admin_update_doctor, name="admin_update_doctor"),
#     path("doctors/<int:doctor_id>/delete/", views.admin_delete_doctor, name="admin_delete_doctor"),
# ]
