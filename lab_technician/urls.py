from django.urls import path
from . import views 

urlpatterns = [
    path("create/", views.create_labtechnician_profile,name="create-lab-technician-pofile"),
    path("profile/", views.labtechnician_self_profile, name="labtechnician-self-profile"),
    path("update/", views.update_labtechnician_profile, name="update-labtechnician-profile"),
    #path("list/", views.list_labtechnicians),
    path("verify/<uuid:user_id>/", views.verify_labtechnician, name="verify-lab-technician"),
]
