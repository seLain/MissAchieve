"""MissAchieve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from rest_framework.authtoken import views
from .views import index
from .views import create_mission, get_mission, update_mission, delete_mission,\
                   get_badges

urlpatterns = [
    path('', index), # achievement root route
    path('api-token-auth/', views.obtain_auth_token),
    path('mission/create', create_mission),
    path('mission/get', get_mission),
    path('mission/update', update_mission),
    path('mission/delete', delete_mission),
    path('badges', get_badges),
]
