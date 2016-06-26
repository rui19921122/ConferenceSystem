"""ConferenceSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from base.views import mainView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api/v2/auth/', include('rest_auth.urls')),
    url(r'^api/v2/class_plan/', include('class_plan.urls')),
    url(r'^api/v2/study/', include('professionalStudy.urls')),
    url(r'^api/v2/menu/', include('base.urls')),
    url(r'^api/v2/worker/', include('worker.urls')),
    url(r'^api/v2/upload/', include('upload.urls')),
    url(r'^api/v2/accident/', include('accidentCase.urls')),
    url(r'^api/v2/call_over/', include('call_over.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', mainView)
]
