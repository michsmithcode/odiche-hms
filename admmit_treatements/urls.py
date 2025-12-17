from django.urls import path
from . import views

urlpatterns = [
    # Admissions
    path("admit/", views.admit_patient),
    path("list/", views.list_admissions),
    path("discharge/<int:admission_id>/", views.discharge_patient),

    # Treatments
    path("treatment/add/", views.add_treatment),
    path("treatment/<int:admission_id>/", views.list_treatments),
]
