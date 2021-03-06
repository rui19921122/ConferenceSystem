from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^get-default-class-number/$', view=GetDefaultClassNumber.as_view(), name='get-default-class-number'),
    url(r'^get-call-over-text/$', view=GetCallOverText.as_view(), name='get-call-over-text'),
    url(r'^end-call-over/$', view=EndCallOver.as_view(), name='end-call-over'),
    url(r'^query-call-over-detail/(?P<id>\d{1,8})/$', view=QueryCallOverByDepartment.as_view(), name='query-call-over'),
    url(r'^list-call-over/$', view=ListClassOverByDepartment.as_view(), name='query-call-over'),
    url(r'^get-call-over-person/$', view=GetCallOverPerson.as_view(), name='get-call-over-person'),
    url(r'^get-call-over-person-detail/$', view=GetCallOverPersonDetail.as_view(), name='get-call-over-person-detail'),
    url(r'^post-figure/$', view=PostFigureData.as_view(), name='post-figure'),
    url(r'^lock-call-over-person/$', view=LockCallOverPerson.as_view(), name='lock-call-over-person'),
    url(r'^update-call-over-person/(?P<id>\d{1,8})/$', view=UpdateCallOverPerson.as_view(),
        name='update-call-over-person'),
    url(r'^add-call-over-person/(?P<id>\d{1,8})/$', view=AddCallOverPerson.as_view(), name='add-call-over-person'),
    url(r'^get-can-add-call-over-person/(?P<id>\d{1,8})/$', view=GetWorkerCanAdd.as_view(),
        name='add-call-over-person'),
    url(r'^call-over-note/$', view=call_over_note, name='call_over_note'),
]
