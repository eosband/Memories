"""project_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from API_proj2app.views import *
from django.conf import settings # for media
from django.conf.urls.static import static


# Fairly standard url requests

urlpatterns = [
    path('', requestHandlers.index),
    path('admin/', admin.site.urls),
    path('login/', requestHandlers.auth_login),
    path('newUser/', requestHandlers.newUser),
    path('memories/', requestHandlers.handleMemories),
    path('logout/', requestHandlers.auth_logout),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) # for media
