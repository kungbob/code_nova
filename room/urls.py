from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accept_help_request/(?P<room_id>\d+)/',views.accept_help_request,name='accept_help_request'),
    url(r'^(?P<room_id>\d+)/',views.room,name='room'),
    url(r'^$', views.list_room, name='list_room'),


]
