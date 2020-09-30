"""online_education URL Configuration

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
from django.urls import path, include
import xadmin
from apps.users.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('users/', include(('apps.users.urls', 'user'), namespace='users')),
    path('courses/', include(('apps.courses.urls', 'course'), namespace='courses')),
    path('orgs/', include(('apps.orgs.urls', 'orgs'), namespace='orgs')),
    path('operations/', include(('operations.urls', 'operations'), namespace='operations')),
    path('', index, name='index'),
    path('captcha/', include('captcha.urls'))
]
