from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic.base import RedirectView
from app import api
from mynode import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mynode/', include('app.urls')),
    url(r'^service/posts/(?P<post_uuid>[-\w]+)$', api.post),
    url(r'^service/author/posts$', api.author_posts),
    url(r'^service/author/(?P<author_id>\w+)/posts$', api.specific_author_posts),
    url(r'^service/posts$', api.posts),
    url(r'^service/friends/(?P<authorUUID>[-\w]+)$', api.friendshipList),
    url(r'^service/friends/(?P<uuidA>[-\w]+)/(?P<uuidB>[-\w]+)$', api.friendship),
    url(r'^service/friendrequest$', api.friendrequest),
    # INSECURE - DO NOT USE UNLESS YOU ARE TESTING! USE STREAM/IMAGE/<IMAGE_ID> INSTEAD.
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^global/authors$', api.get_all_users),
    url(r'^.*$', RedirectView.as_view(url='/mynode/', permanent=False)),
)
