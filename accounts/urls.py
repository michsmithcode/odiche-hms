from django.urls import path
#from .views import UserInviteView
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




#from .views import custom_token_obtain_pair, custom_token_refresh
#from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )





 #from django.urls import path
# from .views import custom_token_obtain_pair, custom_token_refresh

#  urlpatterns = [
      #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

#     path("token/", custom_token_obtain_pair, name="token_obtain_pair"),
#     path("token/refresh/", custom_token_refresh, name="token_refresh"),
# ]