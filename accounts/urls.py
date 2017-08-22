from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts.views import register_view


urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', register_view, name='register'),


]