from django.urls import path
from . import views

urlpatterns = [
    path("doctors/", views.admin_list_doctors, name="admin_list_doctors"),
    path("doctors/<int:doctor_id>/", views.admin_get_doctor, name="admin_get_doctor"),
    path("doctors/<int:doctor_id>/update/", views.admin_update_doctor, name="admin_update_doctor"),
    path("doctors/<int:doctor_id>/delete/", views.admin_delete_doctor, name="admin_delete_doctor"),
]
