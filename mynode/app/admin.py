from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render_to_response
from app.models import *


###########################################
# Custom Display lists for the admin page #
###########################################

#Admin approval action method for approving users
def approve(modeladmin, request, queryset):
    queryset.update(approved=1)
approve.short_description = "Approve the selected Users"

class Posts(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'content_type', 'visibility')

class Comments(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'parent_post')

class Friends(admin.ModelAdmin):
    list_display = ('id', 'requester', 'receiver', 'accepted')

class RemoteServers(admin.ModelAdmin):
    list_display = ('hostname', 'active')

class RemoteFriends(admin.ModelAdmin):
    list_display = ('uuid', 'displayname', 'host', 'remote_accepted', 'local_accepted', 'local_receiver', 'blocked')

class Users_Admin(admin.ModelAdmin):
    list_display = ('user', 'git_url', 'default_post_visibility', 'approved')
    list_filter = ['approved']
    actions = [approve]

#############################################

admin.site.register(Comment,Comments)
admin.site.register(Friend,Friends)
admin.site.register(Image)
admin.site.register(Post,Posts)
admin.site.register(Users,Users_Admin)
# Register your models here.
