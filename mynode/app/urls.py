from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    #url(r'^feed/$', views.feed, name='feed'),
    #url(r'^friends/$', views.friends, name='friends'),
)
