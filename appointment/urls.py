from django.urls import path
from . import views

urlpatterns = [
    # ============================
    # Appointment CRUD
    # ============================
    
    # List all appointments
    path('', views.list_appointments, name='appointments-list'),
    
    # Retrieve a single appointment
    path('<uuid:pk>/', views.appointment_detail, name='appointment-detail'),
    
    # Create new appointment
    path('create/', views.create_appointment, name='appointment-create'),
    
    # Update an appointment (PATCH)
    path('<uuid:pk>/update/', views.update_appointment, name='appointment-update'),
    
    # Delete an appointment
    path('<uuid:pk>/delete/', views.delete_appointment, name='appointment-delete'),
]
