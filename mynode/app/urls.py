from django.conf.urls import patterns, url
from mynode import settings
from app import views
from app import api

urlpatterns = patterns('',
    url(r'^$', views.login),
    url(r'^login/?$','django.contrib.auth.views.login', {'template_name': 'login_page.html'}),
    url(r'^logout/?$', views.logout_view),
    url(r'^register/?$', views.register),
    url(r'^profile/?$', views.profile),
    url(r'^approval_needed/?$', views.approval_needed),
    url(r'^stream/?$', views.stream),
    url(r'^stream/post/(\d+)/$', views.post_details),
    url(r'^stream/post/(\d+)/delete/$', views.delete_post),
    url(r'^stream/post/create/?$', views.create_post),
    url(r'^stream/post/(\d+)/comments/', views.create_comment),
    url(r'^stream/image/(\d+)$',views.image),
    url(r'^stream/image/?$',views.image),
    url(r'^author/(?P<author_id>\w+)/$', views.author_profile),

    url(r'^friends/$', views.friends),
    #url(r'^friends/friend/(\d+)/create/$', views.create_friend),
    # Only used for manual friend requests
    url(r'^friends/friend/create/$', views.create_friend),
    url(r'^friends/(\d+)/confirm/$', views.confirm_friend),
    url(r'^friends/(\d+)/deny/$', views.deny_friend),
    url(r'^friends/(\d+)/delete/$', views.delete_friend),
    #url(r'^friends/friend/friend/(\d+)/$', views.friend_details),
    # Need to create delete_friend_request, and use the method below to remove EXISTING friendships
    url(r'^remote_friends/(?P<uuid>[-\w]+)/delete/$', api.delete_remote_friend),
    url(r'^remote_friends/(?P<uuid>[-\w]+)/confirm/$', api.confirm_remote_friend),
  
)
