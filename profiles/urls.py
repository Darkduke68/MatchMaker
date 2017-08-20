from django.conf.urls import url, include
from profiles.views import profile_update, profile_get

urlpatterns = [
    url(r'^$', profile_get, name='profile'),
    url(r'^update/$', profile_update, name='profile-update'),
    url(r'^avatar/', include('avatar.urls')),


]