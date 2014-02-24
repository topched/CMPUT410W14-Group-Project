from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mynode.views.home', name='home'),
    url(r'^feed/', include('app.urls')),
    url(r'^friends/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
