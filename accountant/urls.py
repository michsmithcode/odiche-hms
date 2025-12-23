from django.urls import path
from . import views

urlpatterns = [
    # Accountant Self control
    path("profile/", views.get_accountant_profile, name="get_accountant_profile"),
    path("profile/update/", views.update_accountant_profile, name="update_accountant_profile"),

    # Admin-only controls
    path("profile/admin/list/", views.admin_list_accountants, name="admin_list_accountants"),
    path("profile/admin/<str:accountant_id>/", views.admin_get_accountant, name="admin_get_accountant"),
    path("profile/admin/<str:accountant_id>/update/", views.admin_update_accountant, name="admin_update_accountant"),
    path("profile/admin<str:accountant_id>/delete/", views.delete_accountant_profile, name="delete_accountant_profile"),
]


