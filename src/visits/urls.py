from django.contrib import admin
from django.urls import path

from .views import home_view, about_view

app_name = "visits"

urlpatterns = [
    path("about/", about_view, name="about"),
]
