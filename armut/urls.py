"""armut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,re_path
import app.views
from rest_framework import viewsets
from knox import views as knox_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^register/', app.views.RegisterAPI.as_view(), name='register'),
    re_path(r'^message/', app.views.messages.as_view(), name='message'),
    re_path(r'^block/', app.views.blocks.as_view(), name='block'),
    re_path(r'^log/', app.views.logs.as_view(), name='log'),
    re_path(r'^login/', app.views.LoginAPI.as_view(), name='login'),
    re_path(r'^logout/', knox_views.LogoutView.as_view(), name='logout'),
    re_path(r'^logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
