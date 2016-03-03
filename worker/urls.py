from django.conf.urls import include, url
from django.contrib import admin
from .views import WorkerDetailView, WorkerView

urlpatterns = [
    url(r'^worker/', view=WorkerView.as_view(), name='worker_list'),
    url(r'^worker/(?P<pk>\d{1,5})/', view=WorkerDetailView.as_view(), name='worker_detail')
]
