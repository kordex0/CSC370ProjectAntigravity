from django.conf.urls import url

from . import views

urlpatterns = [
    # first: regex
    # second: calls specified view function with an HttpRequest object as the first argument and any captured values from the regular expresion: ?P<...>
    # third: name the url for better use in templates
    url(r'^/$', views.index, name='index'),
    # ?P<id> pass id as keyword argument to function views.course
    url(r'^(?P<id>[0-9]+)/$', views.assignment, name='detail'),
]
