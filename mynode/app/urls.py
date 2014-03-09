from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^register/$', views.register),
    url(r'^$', 'django.contrib.auth.views.login'),

    url(r'^stream/$', views.stream),
    url(r'^stream/post/(\d+)/$', views.post_details),
    url(r'^stream/post/(\d+)/delete/$', views.delete_post),
    url(r'^stream/post/create/$', views.create_post),
    url(r'^stream/post/(\d+)/comments/', views.create_comment),

    url(r'^friends/$', views.friends),
    #url(r'^friends_requests/', views.friends.create_friendRequest),
)
