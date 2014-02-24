from django.conf.urls import patterns, url

#from app import views

urlpatterns = patterns('',
        # ex: /feed/
        url(r'^feed/', views.feed, name='feed'),
        url(r'^friends/', views.friends, name='friends'),
        url(r'^admin/', include(admin.site.urls)),
)
