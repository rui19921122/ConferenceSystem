from django.conf.urls import include, url
from django.contrib import admin
from .views import Menu

urlpatterns = [
    url(r'^get-menu', view=Menu.as_view(), name='getMenu'),
]
