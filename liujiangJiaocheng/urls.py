# -*- coding: utf-8 -*-
"""liujiangJiaocheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from combatOne import views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'register/', views.register),
    url(r'logout/', views.logout),
    url(r'^confirm/$',views.user_confirm),
    # 在根目录下的urls.py文件中增加captcha对应的网址
    # 由于是用来二级路由机制，需要在顶部 from django.conf.urls import include
    url(r'captcha',include('captcha.urls'))
]
