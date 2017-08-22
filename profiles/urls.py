from django.conf.urls import url, include
from profiles.views import profile_update, profile_get, profile_single

urlpatterns = [
    url(r'^$', profile_get, name='profile'),
    url(r'^(?P<pk>\d+)/$', profile_single, name='profile-single'),
    url(r'^update/$', profile_update, name='profile-update'),
    url(r'^avatar/', include('avatar.urls')),

]