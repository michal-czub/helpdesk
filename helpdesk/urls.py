"""helpdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import django.conf
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('project.urls')),
    path('boards/', include('board.urls')),
    path('stages/', include('stage.urls')),
    path('applications/', include('application.urls')),
    path('teams/', include('team.urls')),
    path('staffs/', include('staff.urls')),
    path('events/', include('event.urls')),
    path('clients/', include('client.urls')),
]
if django.conf.settings.DEBUG:
    urlpatterns += static(django.conf.settings.MEDIA_URL, document_root=django.conf.settings.MEDIA_ROOT)
