from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'login_page.html'}),
    url(r'^register/$', views.register),
    url(r'^profile/$', views.profile),
    url(r'^stream/$', views.stream),
    url(r'^stream/post/(\d+)/$', views.post_details),
    url(r'^stream/post/(\d+)/delete/$', views.delete_post),
    url(r'^stream/post/create/$', views.create_post),
    url(r'^stream/post/(\d+)/comments/', views.create_comment),

    url(r'^friends/$', views.friends),
    url(r'^friends/friend/create/$', views.create_friend),
    #url(r'^friends_requests/', views.friends.create_friendRequest),
)
