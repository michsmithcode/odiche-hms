from django.urls import path
from . import views

urlpatterns = [
     # Nurse 
    path('profile/', views.nurse_view_profile, name='nurse_self_profile'),
    path("records/", views.record_vitals, name="record_vitals"),
    # Admin
    path('admin/nurses/', views.admin_list_nurses, name='admin_list_nurses'),
    path('admin/nurse/create/', views.admin_create_nurse, name='admin_create_nurse'),
    path('admin/nurse/update/<int:nurse_id>/', views.admin_update_nurse, name='admin_update_nurse'),
    path('admin/nurse/delete/<int:nurse_id>/', views.admin_delete_nurse, name='admin_delete_nurse'),

   
    
]
