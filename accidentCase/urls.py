from django.conf.urls import include, url
from django.contrib import admin
from .views import AccidentView, AccidentDetailView, GetUnlearnedAccident

urlpatterns = [
    url(r'^accident/$', view=AccidentView.as_view(), name='accident'),
    url(r'^accident/(?P<pk>\d{1,6})$', view=AccidentDetailView.as_view(),
        name='accident-detail'),
    url(r'^get-unlearned-accident/$', view=GetUnlearnedAccident.as_view(),
        name='accident-unlearned'),
]
