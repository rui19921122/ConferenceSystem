from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^get-default-class-number/$', view=GetDefaultClassNumber.as_view(), name='get-default-class-number'),
    url(r'^begin-call-over/$', view=BeginCallOver.as_view(), name='begin-call-over'),
]
