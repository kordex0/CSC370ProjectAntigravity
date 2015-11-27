from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='user_login'),
    url(r'^logout/$', auth_views.logout_then_login, name='user_logout'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^new_user/$', views.new_user, name='new_user'),
]
