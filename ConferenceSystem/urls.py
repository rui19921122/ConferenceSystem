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
from django.conf.urls import include, url
from django.contrib import admin

api_url = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^class_plan/', include('class_plan.urls')),
    url(r'^study/', include('professionalStudy.urls')),
    url(r'^menu/', include('base.urls')),
    url(r'^worker/', include('worker.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^accident/', include('accidentCase.urls')),
]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_url)),
    url(r'^', include('rest_framework_docs.urls')),
]
