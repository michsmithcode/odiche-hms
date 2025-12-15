from django.urls import path
from .views import shift_list_create, shift_detail, list_shifts

urlpatterns = [
    path("shifts/", shift_list_create, name="shift-list-create"),
    path("shifts/", list_shifts, name="shift_list"),
    path("shifts/<uuid:shift_id>/", shift_detail, name="shift-detail"),
]
