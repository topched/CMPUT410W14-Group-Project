from django.conf.urls import patterns, url

#from app import views

urlpatterns = patterns('',
        url(r'^feed/', include('feed.urls')),
        url(r'^friends/', include('friends.urls')),
        url(r'^admin/', include(admin.site.urls)),
)
