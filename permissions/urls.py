from django.urls import path
from . import views
from .decorators import admin_only
#from .views import admin_manage_roles


urlpatterns = [
    # ------------------- PERMISSION CRUD -------------------
    #path("permissions/", views.list_permissions, name="list_permissions"),
    path("permissions/create/", views.create_permission, name="create_permission"),
    path("permissions/<int:pk>/update/", views.update_permission, name="update_permission"),
    path("permissions/<int:pk>/delete/", views.delete_permission, name="delete_permission"),
    # ------------------- ROLE CRUD -------------------
    path("roles/", views.list_roles, name="list_roles"),
    path("roles/create/", views.create_role, name="create_role"),
    path("roles/<int:pk>/update/", views.update_role, name="update_role"),
    path("roles/<int:pk>/delete/", views.delete_role, name="delete_role"),
    # ------------------- TOGGLE ROLE PERMISSION -------------------
    path("roles/permissions/toggle/", views.enable_or_disable_role_permission, name="toggle_role_permission"),
    # ------------------- GET ROLE PERMISSIONS -------------------
    path("roles/permissions/list/", views.get_role_permissions, name="get_role_permissions"),
    
     # PERMISSION MANAGEMENT API
    # -------------------------
    path("permissions/", admin_only(views.list_permissions), name="list_permissions"),
    #path("permissions/toggle/", admin_only(views.toggle_role_permission), name="toggle_role_permission"),
    path("permissions/role/<str:role>/", admin_only(views.get_role_permissions), name="get_role_permissions"),
    #path("permissions/user/<int:user_id>/", admin_only(views.get_user_permissions), name="get_user_permissions"),

    # Optional helper for checking user permissions
    #path("permissions/check/", views.check_permission, name="check_permission"),
    
    #=============================ADMIN TEST PERMISSION================
    path("test-system/", views.test_permissions_system, name="test_permissions_system"),
    #================= Use: GET /permissions/test-system/
                            #Authorization: Bearer <access_token>
]



#===============================End================

# urlpatterns = [
#     path('toggle/', views.enable_or_disable_role_permission, name='permissions-toggle'),
#     path('role-perms/', views.get_role_permissions, name='permissions-role-list'),
#     path("admin/manage-roles/", views.admin_manage_roles),
    
    
# ]



# urlpatterns = [
#     # Doctor
#     path('doctor/prescriptions/', views.doctor_prescription_view, name='doctor-prescription'),
    #path('doctor/patients/', views.doctor_view_patients, name='doctor-view-patients'),

    # # Nurse
    # path('nurse/update-vitals/', views.nurse_update_vitals, name='nurse-update-vitals'),
    # path('nurse/assist-doctor/', views.nurse_assist_doctor, name='nurse-assist-doctor'),

    # # Pharmacist
    # path('pharmacist/dispense/', views.pharmacist_dispense_medicine, name='pharmacist-dispense'),
    # path('pharmacist/inventory/', views.pharmacist_manage_inventory, name='pharmacist-inventory'),

    # # Pharmacy Cashier
    # path('cashier/payment/', views.pharmacy_cashier_process_payment, name='cashier-payment'),

    # # Hospital Admin
    # path('hospitaladmin/manage-staff/', views.hospital_admin_manage_staff, name='hospitaladmin-manage-staff'),
    # path('hospitaladmin/reports/', views.hospital_admin_view_reports, name='hospitaladmin-reports'),

    # # Main Admin
    # path('mainadmin/manage/', views.main_admin_manage_all, name='mainadmin-manage'),

    # # Patient
    # path('patient/record/', views.patient_record_view, name='patient-record'),
#]


# urlpatterns = [
#     path('doctor/prescriptions/', views.doctor_prescription_view, name='doctor-prescriptions'),
#     path('pharmacy/inventory/', views.pharmacy_inventory_view, name='pharmacy-inventory'),
#     path('patient/record/', views.patient_record_view, name='patient-record'),
# ]
