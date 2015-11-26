from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)/$', views.course, name='detail'),
    url(r'^section/(?P<id>[0-9]+)/$', views.section_detail, name='section_detail'),
    url(r'^section/(?P<section_id>[0-9]+)/assignments/$', views.assignment, name='assignment_index'),
    url(r'^section/assignments/(?P<assignment_id>[0-9]+)$', views.assignment_detail, name='assignment_detail'),
    url(r'^add_course/$', views.add_course, name="add_course"),
    url(r'^(?P<course_id>[0-9]+)/delete_course/$', views.delete_course, name="delete_course"),
    url(r'^(?P<course_id>[0-9]+)/add_section/$', views.add_section, name='add_section'),
    
]
