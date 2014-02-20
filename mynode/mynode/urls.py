from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mynode.views.home', name='home'),
    url(r'^feed/', include('feed.urls')),
    url(r'^friends/', include('friends.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
