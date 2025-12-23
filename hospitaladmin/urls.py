from django.urls import path
from . import views
from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.create_hospital_admin_profile, name="create-hospital-admin-profile"),
    path("profile/", views.hospital_admin_self_profile, name="hostpital-admin-self-profile"),
    path("update/", views.update_hospital_admin_profile, name="update-hospital-admin-profile"),
    #path("list/", views.list_hospital_admins),
    path("verify/<uuid:user_id>/", views.verify_hospital_admin, name="verify-hospital-admin-profile"),
]
