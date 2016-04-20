from django.conf.urls import include, url
from django.contrib import admin
from .views import WorkerDetailView, WorkerView, PositionListView, PositionDetailView, FigureCollect

urlpatterns = [
    url(r'^worker/$', view=WorkerView.as_view(), name='worker_list'),
    url(r'^worker/(?P<pk>\d{1,9})/', view=WorkerDetailView.as_view(), name='worker_detail'),
    url(r'^position/$', view=PositionListView.as_view(), name='position_list'),
    url(r'^position/(?P<pk>\d{1,9})/', view=PositionDetailView.as_view(), name='position_detail'),
    url(r'^figure-post/$', view=FigureCollect.as_view(), name='figure-post'),
]
