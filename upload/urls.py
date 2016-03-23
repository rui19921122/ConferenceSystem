from django.conf.urls import include, url
from django.contrib import admin
from .views import handleClassPlanFile, handleUploadImage,handleUploadAudio

urlpatterns = [
    url(r'^class-plan/(?P<date>\d{4}-\d{1,2}-\d{1,2})', view=handleClassPlanFile, name='getMenu'),
    url(r'^call-over-image/(?P<id>\d{1,6})/$', view=handleUploadImage.as_view(), name='upload-image'),
    url(r'^call-over-audio/(?P<id>\d{1,6})/$', view=handleUploadAudio, name='upload-audio'),
]
