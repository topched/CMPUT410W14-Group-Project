from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'login_page.html'}),
    url(r'^stream/$', views.stream, {'template_name': 'stream_page.html'}),
    url(r'^register/$', views.register, {'template_name': 'registration_page.html'}),
    url(r'^friends/$', views.friends, {'template_name':'friend_page.html'}),
    #url(r'^feed/$', views.feed, name='feed'),
)
