from django.urls import path
from .import views
from utilsapp.views import resend_otp_view
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("invite/", views.invite_user, name="user-invite"),
    path("activate/", views.activate_invite, name="activate_invite"),
    path("verify/", views.verify_otp_code, name="verify_otp"),
    path("resend_otp/", resend_otp_view, name="resend_otp"),
    path("login/", views.login_user, name="login_user"),
    
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]

