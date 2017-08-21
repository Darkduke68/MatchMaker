from django.conf.urls import url
from .views import questions, question_single

urlpatterns = [
    url(r'^$', questions, name='questions'),
    url(r'^(?P<pk>\d+)/$', question_single, name='question_single'),

]