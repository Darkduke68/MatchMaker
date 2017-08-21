from django.conf.urls import url
from .views import question

urlpatterns = [
    url(r'^$', question, name='question')
]