"""hotelinfo_manage URL Configuration

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
from django.urls import path,include
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页路由
    path('',views.index),
    # 前端+用户的登录注册和后台 路由  反向解析
    path('',include(('main.urls','main'),namespace='main')),
    # 酒店后台
    path('merchants/',include(('hotel.urls','hotel'),namespace='hotel')),
    # 流媒体和静态文件路由
    url(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
