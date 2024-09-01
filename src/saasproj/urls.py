"""
URL configuration for saasproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import pw_protected_view, user_only_view

urlpatterns = [
    path("", include("auth_app.urls")),
    path("", include("visits.urls")),
    path("", include("subscriptions.urls")),
    path("", include("homepage.urls")),
    path("", include("checkouts.urls")),
    path("", include("landing.urls")),
    path("protected/", pw_protected_view),
    path("protected/user-only", user_only_view),
    path("accounts/", include("allauth.urls")),
    path("profiles/", include("profiles.urls")),
    path("admin/", admin.site.urls, name="admin"),
]
