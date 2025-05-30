"""gym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from gym_auth import views as auth_views

urlpatterns = [
    path('admin/dashboard/', include('main.urls_admin')),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('gym_auth.urls')),  # Updated path
    path('auth/', include('django.contrib.auth.urls')),  # Built-in auth    
    path('profile/', auth_views.profile, name='profile'),
] 