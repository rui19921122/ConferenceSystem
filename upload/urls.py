from django.conf.urls import include, url
from django.contrib import admin
from .views import handleClassPlanFile, handleUploadImage,handleUploadAudio,handleUploadAccident,deleteUploadAccident

urlpatterns = [
    url(r'^class-plan/(?P<date>\d{4}-\d{1,2}-\d{1,2})', view=handleClassPlanFile, name='getMenu'),
    url(r'^call-over-image/(?P<id>\d{1,6})/$', view=handleUploadImage, name='upload-image'),
    url(r'^call-over-audio/(?P<id>\d{1,6})/$', view=handleUploadAudio, name='upload-audio'),
    url(r'^accident-file/(?P<id>\d{1,6})/$', view=handleUploadAccident, name='upload-accident'),
    url(r'^delete-accident-files/(?P<id>\d{1,6})/$', view=deleteUploadAccident, name='delete-accident-file'),
]
