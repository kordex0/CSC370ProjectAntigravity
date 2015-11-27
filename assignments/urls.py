from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.assignment_index, name='index'),
    url(r'^(?P<assignment_id>[0-9]+)/$', views.assignment_detail, name='detail'),
]
