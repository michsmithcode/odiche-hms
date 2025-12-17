from django.urls import path
from .import views 

urlpatterns = [
    path("create/", views.ward_list_create, name="ward-list-create"),
    path("update/<int:pk>/", views.ward_detail, name="ward-detail"),
    path("beds_create/", views.bed_create, name="create_bed"),
]
