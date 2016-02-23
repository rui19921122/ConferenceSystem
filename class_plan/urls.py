from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ClassPlanBaseViewSet, ClassPlan

router = DefaultRouter()
router.register('classPlanBase', ClassPlanBaseViewSet, base_name='class-plan-base')
urlpatterns = [url(r'^', include(router.urls))]
urlpatterns += [
    url(r'^classPlan/(?P<date>\d{8})', name='class-plan', view=ClassPlan.as_view()),
]
