from django.conf.urls import url
from .views import questions, question_single, questions_update

urlpatterns = [
    url(r'^$', questions, name='questions'),
    url(r'^update/$', questions_update, name='questions-update'),
    url(r'^(?P<pk>\d+)/$', question_single, name='question-single'),

]