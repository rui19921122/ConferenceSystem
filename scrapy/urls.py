from django.conf.urls import url, include
from .views import GetId, SetPasswordView

urlpatterns = [
    url(r'^get-station-text/$',
        view=GetId.as_view(), name='get-id'),  # 获取路局网站信息
    url(r'^about-password/$',
        view=SetPasswordView.as_view(), name='about-password'),  # 获取路局网站信息
]
