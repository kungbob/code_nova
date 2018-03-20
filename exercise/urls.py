from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<exercise_id>\d+)',views.exercise,name='exercise'),
    url(r'^$', views.list_exercise,name='list_exercise'),
    url(r'^start_exercise/(?P<exercise_id>\d+)',views.start_exercise,name='start_exercise'),
    url(r'^statistics/(?P<exercise_id>\d+)',views.statistics,name='statistics'),

]
