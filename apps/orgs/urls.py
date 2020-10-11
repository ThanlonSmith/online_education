"""online_classroom_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from .views import org_list, org_home, org_course, org_desc, org_teacher

urlpatterns = [
    path('list/', org_list, name='org_list'),
    re_path('^home/(\d+)/$', org_home, name='org_home'),
    re_path('^course/(\d+)/$', org_course, name='org_course'),
    re_path('^desc/(\d+)/$', org_desc, name='org_desc'),
    re_path('^teacher/(\d+)/$', org_teacher, name='org_teacher'),
]
