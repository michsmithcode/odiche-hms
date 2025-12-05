from django.urls import path
from . import views

urlpatterns = [

    # MEDICAL HISTORY URL
    path("medical-history/", views.medical_history_list_create, name="medical-history-list"),
    path("medical-history/<int:pk>/", views.medical_history_detail, name="medical-history-detail"),

    # PATIENT VITALS URL
    path("vitals/", views.patient_vital_list_create, name="vitals-list"),
    path("vitals/<int:pk>/", views.patient_vital_detail, name="vitals-detail"),

    #PATIENT VISITS URL
    path("visits/", views.patient_visit_list_create, name="visits-list"),
    path("visits/<int:pk>/", views.patient_visit_detail, name="visits-detail"),
]
