from django.conf.urls import include
from django.urls import path

from .views import LoginAPIView, RegisterAPIView, LogoutAPIView, UserDetailsAPIView

auth_enpoints = [
    path('login',  LoginAPIView.as_view(), name="login"),
    path('register',  RegisterAPIView.as_view(), name="register"),
    path('logout',  LogoutAPIView.as_view(), name="logout"),
    path('profile',  UserDetailsAPIView.as_view(), name="profile")
]

urlpatterns = [
    path('userauth/', include(auth_enpoints))
]