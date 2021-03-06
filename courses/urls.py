
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.course_index, name='index'),
    url(r'^(?P<course_id>[0-9]+)/$', views.course_detail, name='detail'),
    url(r'^add_course/$', views.add_course, name="add_course"),
    url(r'^section/(?P<id>[0-9]+)/$', views.section_detail, name='section_detail'),
    url(r'^section/(?P<section_id>[0-9]+)/assignments/$', views.assignment_index, name='assignment_index'),
    url(r'^section/assignments/(?P<assignment_id>[0-9]+)$', views.assignment_detail, name='assignment_detail'),
    url(r'^section/(?P<section_id>[0-9]+)/new_assignment/$', views.new_assignment, name='new_assignment'),
    url(r'^(?P<course_id>[0-9]+)/delete_course/$', views.delete_course, name="delete_course"),
    url(r'^(?P<course_id>[0-9]+)/add_section/$', views.add_section, name='add_section'),
    url(r'^(?P<section_id>[0-9]+)/enroll/$', views.enroll, name='enroll'),
]
