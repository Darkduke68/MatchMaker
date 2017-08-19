from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts.views import register_view


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', register_view, name='register'),


]