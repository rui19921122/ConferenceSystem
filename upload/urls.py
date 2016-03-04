from django.conf.urls import include, url
from django.contrib import admin
from .views import handleClassPlanFile

urlpatterns = [
    url(r'^class-plan/(?P<date>\d{4}-\d{1,2}-\d{1,2})', view=handleClassPlanFile, name='getMenu'),
]
