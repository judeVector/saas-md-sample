from django.urls import path
from .views import landing_dashboard_page_view

app_name = "landing_page"


urlpatterns = [path("", landing_dashboard_page_view, name="landing")]
