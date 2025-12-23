from django.urls import path
from . import views 


urlpatterns = [
    path("order/", views.order_lab_test, name="order-lab-test"),
    path("pending/", views.pending_lab_tests, name="pending-lab-test"),
    path("result/upload/<int:test_id>/", views.upload_lab_result, name="upload-lab-test"),
    path("result/verify/<int:result_id>/", views.verify_lab_result, name="verify-lab-result"),
    path("patient/<int:patient_id>/", views.patient_lab_results, name="patient-lab-result"),
]
