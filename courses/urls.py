from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)/$', views.course, name='detail'),
    url(r'^section/(?P<id>[0-9]+)/$', views.section_detail, name='section_detail'),
]
