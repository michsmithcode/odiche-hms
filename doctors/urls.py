from django.urls import path
from . import views


urlpatterns = [
    path("verify-license/", views.verify_license, name="verify-license"),
    #path("auth/test/", views.test_auth),
    path("prescriptions/", views.prescribe_drugs, name="prescribe_medicine"),
    path("consultation/", views.create_consultation, name="create_consultation"),
    #for doctors
    path("profile/", views.get_doctor_profile, name="get_doctor_profile"),
    
    #path("profile/create/", create_doctor_profile, name="create_doctor_profile"),
    path("profile/update/", views.update_doctor_profile, name="update_doctor_profile"),
    path("profile/delete/", views.delete_doctor_profile, name="delete_doctor_profile"),
    #admin only approval
    path("doctors/", views.admin_list_doctors, name="admin_list_doctors"),
    path("doctors/<int:doctor_id>/", views.admin_get_doctor, name="admin_get_doctor"),
    path("doctors/<int:doctor_id>/update/", views.admin_update_doctor, name="admin_update_doctor"),
    path("doctors/<int:doctor_id>/delete/", views.admin_delete_doctor, name="admin_delete_doctor"),
]





#OTPcode: 834979

#http://127.0.0.1:8000/doctors/prescriptions/












# from django.urls import path
# # #from .views import DoctorInviteView
# from .import views


# urlpatterns = [
#     path("invite/", views.invite_doctor, name="doctor-invite"),
#     #path("invite/", DoctorInviteView.as_view(), name="doctor-invite"),
# ]
