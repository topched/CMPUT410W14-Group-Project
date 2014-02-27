from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',

    url(r'^$', views.login, name='login'),
    #url(r'^feed/$', views.feed, name='feed'),
    #url(r'^friends/$', views.friends, name='friends'),
)
