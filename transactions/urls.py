from django.urls import path
from .import views

urlpatterns = [
    path("invoice/create/", views.create_invoice, name="create-invoice"),
    path("create/", views.create_transaction, name="create-transaction"),
    path("verify/<int:transaction_id>/", views.verify_transaction, name="verify-transaction"),
    path("payment/record/", views.record_payment, name="record-payment"),
]
