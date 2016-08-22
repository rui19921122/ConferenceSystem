from django.conf.urls import include, url
from .views import QueryList,QueryDetail

urlpatterns = [
    url('query-call-over', QueryList.as_view(), name='query-call-over'),
    url('query-detail/(\d*?)/$', QueryDetail.as_view(), name='query-detail')
]