from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^get-default-class-number/$', view=GetDefaultClassNumber.as_view(), name='get-default-class-number'),
    url(r'^begin-call-over/$', view=BeginCallOver.as_view(), name='begin-call-over'),
    url(r'^query-call-over-detail/(?P<id>\d{1,8})/$', view=QueryCallOverByDepartment.as_view(), name='query-call-over'),
    url(r'^list-call-over/', view=ListClassOverByDepartment.as_view(), name='query-call-over'),
]
