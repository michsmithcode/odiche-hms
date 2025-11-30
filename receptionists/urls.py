from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.get_receptionist_profile, name="receptionist_profile"),
    path("profile/create/", views.create_receptionist_profile, name="create_receptionist_profile"),
    path("profile/update/", views.update_receptionist_profile, name="update_receptionist_profile"),
    path("profile/delete/", views.delete_receptionist_profile, name="delete_receptionist_profile"),
]
