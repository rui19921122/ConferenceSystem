from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^ClassPlanBase/$', views.updateClassPlanBase.as_view(),
        name='update_class_plan'),
    url(r'^ClassPlanBase/(?P<pk>\d*)', views.getClassPlanBaseByPk.as_view(),
        name='get_class_plan'),
]
