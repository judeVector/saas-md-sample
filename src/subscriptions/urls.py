from django.urls import path
from .views import subscription_price_view

app_name = "subscriptions"

urlpatterns = [
    path("pricing/", subscription_price_view, name="pricing"),
]
