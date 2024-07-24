from django.urls import path
from .views import login_view, register_view

app_name = "auth_app"

urlpatterns = [
    path("accounts/login", login_view, name="login"),
    path("register/", register_view, name="register"),
]
