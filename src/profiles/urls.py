from django.urls import path, include
from . import views


urlpatterns = [
    path("detail/", views.profile_detail_view),
    path("<username>/", views.profile_view),
]
