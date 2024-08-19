from django.contrib import admin
from django.urls import path

from .views import home_view, about_view
from landing.views import landing_dashboard_page_view

app_name = "visits"

urlpatterns = [
    path("", landing_dashboard_page_view, name="home"),
    path("about/", about_view, name="about"),
]
