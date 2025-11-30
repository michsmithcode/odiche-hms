from django.urls import path
from .views import shift_list_create, shift_detail

urlpatterns = [
    path("shifts/", shift_list_create, name="shift-list-create"),
    path("shifts/<uuid:shift_id>/", shift_detail, name="shift-detail"),
]
