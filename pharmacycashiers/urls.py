# pharmacy_cashier/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    # =============================
    # Cashier Self-Profile CRUD
    # =============================
    path('profile/', views.cashier_profile, name='cashier-profile'),

    # =============================
    # Admin-Level CRUD
    # =============================
    path('admin/cashiers/', views.admin_cashier_list_create, name='admin-cashier-list-create'),
    path('admin/cashiers/<uuid:pk>/', views.admin_cashier_detail, name='admin-cashier-detail'),
     # =============================
    # Cashier self-service
     # =============================
    path("profile/transactions/", views.cashier_transactions, name="cashier_transactions"),
    path("profile/transactions/create/", views.create_transaction, name="create_transaction"),
     # =============================
    # Admin CRUD
     # =============================
    path("admin/transactions/", views.admin_list_transactions, name="admin_list_transactions"),
    path("admin/transactions/<int:pk>/", views.admin_get_transaction, name="admin_get_transaction"),
    path("admin/transactions/<int:pk>/update/", views.admin_update_transaction, name="admin_update_transaction"),
    path("admin/transactions/<int:pk>/delete/", views.admin_delete_transaction, name="admin_delete_transaction"),
]

