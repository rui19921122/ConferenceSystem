from django.conf.urls import include, url
from django.contrib import admin
from .views import Menu,get_user_detail

urlpatterns = [
    url(r'^get-menu', view=Menu.as_view(), name='get-menu'),
    url(r'^get-user-detail', view=get_user_detail.as_view(), name='get-user-detail'),
]
