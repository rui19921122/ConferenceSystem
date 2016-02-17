from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^updateClassPlan/', views.UpdateClassPlanBase.as_view(),
        name='update_class_plan'),
]
