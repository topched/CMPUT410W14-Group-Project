from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mynode/', include('app.urls')),
    url(r'^.*$', RedirectView.as_view(url='/mynode/', permanent=False), name='index')
)
