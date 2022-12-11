from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import CustomLoginForm
from .views import SignUpView


app_name = "users"
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(authentication_form=CustomLoginForm), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]