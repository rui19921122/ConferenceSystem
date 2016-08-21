from django.conf.urls import include, url
from .views import QueryList

urlpatterns = [
    url('query-call-over', QueryList.as_view(), name='query-call-over')
]