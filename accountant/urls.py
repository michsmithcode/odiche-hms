# from django.urls import path
# from . import views

# urlpatterns = [
#     # Accountant Self Service
#     path("profile/", views.get_accountant_profile, name="get_accountant_profile"),
#     path("profile/update/", views.update_accountant_profile, name="update_accountant_profile"),

#     # Admin-only controls
#     path("all/", views.admin_list_accountants, name="admin_list_accountants"),
#     path("<str:accountant_id>/", views.admin_get_accountant, name="admin_get_accountant"),
#     path("<str:accountant_id>/update/", views.admin_update_accountant, name="admin_update_accountant"),
#     path("<str:accountant_id>/delete/", views.delete_accountant_profile, name="delete_accountant_profile"),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [

#     # Accountant Section
#     path("accountants/create/", views.create_accountant),
#     path("accountants/", views.list_accountants),

#     # Invoices
#     path("invoice/create/", views.create_invoice),

#     # Payments
#     path("payment/make/", views.make_payment),

# ]
