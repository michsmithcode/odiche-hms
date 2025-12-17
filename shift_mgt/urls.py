from django.urls import path
from .import views 

urlpatterns = [
    path("shifts/", views.shift_list_create, name="shift-list-create"),
    path("shifts/", views.list_shifts, name="shift_list"),
    path("shifts/<uuid:shift_id>/", views.shift_detail, name="shift-detail"),
]
