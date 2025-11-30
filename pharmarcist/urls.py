# pharmacist/urls.py
from django.urls import path
from . import views

# urlpatterns = [
   
#     path("admin/pharmacists/", views.admin_list_pharmacists, name="admin_list_pharmacists"),
# ]



urlpatterns = [
     path("pharmacist/profile/", views.pharmacist_profile, name="pharmacist_profile"),
    
    #admin section
    path("admin/pharmacists/", views.admin_list_pharmacists, name="admin_list_pharmacists"),
    path("admin/pharmacists/create/", views.admin_create_pharmacist, name="admin_create_pharmacist"),
    path("admin/pharmacists/<int:pk>/", views.admin_get_pharmacist, name="admin_get_pharmacist"),
    path("admin/pharmacists/<int:pk>/update/", views.admin_update_pharmacist, name="admin_update_pharmacist"),
    path("admin/pharmacists/<int:pk>/delete/", views.admin_delete_pharmacist, name="admin_delete_pharmacist"),
]
