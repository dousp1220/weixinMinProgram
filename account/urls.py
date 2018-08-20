# coding: utf-8
from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'login', views.onAppLogin),
    url(r'hello', views.hello),
]