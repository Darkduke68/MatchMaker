from django.conf.urls import url, include
from profiles.views import profile_update

urlpatterns = [
    #url(r'^$', profile, name='profile'),
    url(r'^update/$', profile_update, name='profile-update'),
    url(r'^avatar/', include('avatar.urls')),


]