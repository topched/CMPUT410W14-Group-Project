from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic.base import RedirectView
from app import api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mynode/', include('app.urls')),
    url(r'^service/post/(?P<post_id>\w+)/$',api.post),
    url(r'^.*$', RedirectView.as_view(url='/mynode/', permanent=False), name='index'),

)
