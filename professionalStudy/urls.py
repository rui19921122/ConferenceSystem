from django.conf.urls import url, include
from .views import ProfessionalStudy, ProfessionalStudyDetail

urlpatterns = [
    url(r'^professional-study', view=ProfessionalStudy.as_view(), name='professionalStudy'),
    url(r'^professional-study/(?P<id>\d{1,3})', view=ProfessionalStudyDetail.as_view(), name='professionalStudyDetail'),
    url(r'^professional-study-post-study/', view=ProfessionalStudyDetail.as_view(), name='professionalStudyPostStudy'),
]
