from django.conf.urls import url, include
from .views import ProfessionalStudy, ProfessionalStudyDetail, GetUnlearnedStudy

urlpatterns = [
    url(r'^professional-study/$', view=ProfessionalStudy.as_view(), name='professionalStudy'),
    url(r'^professional-study/(?P<pk>\d{1,10})', view=ProfessionalStudyDetail.as_view(),
        name='professionalStudyDetail'),
    url(r'^professional-study-post-study/', view=ProfessionalStudyDetail.as_view(), name='professionalStudyPostStudy'),
    url(r'^get-unlearned-study/$', view=GetUnlearnedStudy.as_view(), name='getUnlearnedStudy')
]
