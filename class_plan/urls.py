from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ClassPlanBaseViewSet, ClassPlan, ClassPlanByDate, ClassPlanDetailViewSet

router = DefaultRouter()
urlpatterns = [
    url(r'^classPlan/(?P<date>\d{4}-\d{1,2}-\d{1,2})', name='class-plan-by-date', view=ClassPlanByDate.as_view()),
    url(r'^classPlan/$', name='class-plan', view=ClassPlan.as_view()),
]
#todo 理解router
router.register('classPlanBase', ClassPlanBaseViewSet, base_name='class-plan-base')
router.register('classPlanDetail', ClassPlanDetailViewSet, base_name='class-plan')
urlpatterns += [url(r'api/class_plan',include(router.urls))]