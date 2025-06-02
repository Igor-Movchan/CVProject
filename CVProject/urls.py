"""
URL configuration for CVProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from main.views import cv_list, cv_detail, cv_pdf, recent_requests, settings_view
from rest_framework import routers
from main.api_views import CVViewSet

router = routers.DefaultRouter()
router.register(r"api/cvs", CVViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", cv_list, name="cv_list"),
    path("cv/<int:pk>/", cv_detail, name="cv_detail"),
    path("cv/<int:pk>/pdf/", cv_pdf, name="cv_pdf"),
    path("", include(router.urls)),
    path("logs/", recent_requests, name="recent_requests"),
    path("settings/", settings_view, name="settings"),
]
