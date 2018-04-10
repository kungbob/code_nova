from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^login$', views.login, name='login'),
    url(r'^register_success$', views.register_success, name='register_success'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^myprofile$', views.myprofile, name='myprofile'),

]
