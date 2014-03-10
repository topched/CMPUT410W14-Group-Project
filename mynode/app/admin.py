from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render_to_response
from app.models import *

#class ApproveUsersInline(admin.StackedInline):
#    model = models.OneToOneField(Users)
#    max_num = 1
#    can_delete = False

#class ApproveUsers(admin.ModelAdmin):
#    inlines = [ApproveUsersInline]
#    list_display = ('user', 'approved')
#    def queryset(self, request):
#        qs = super(ApproveUsers, self).queryset(request)
#        return qs.filter(approved=0)

class Posts(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'content_type', 'visibility')

class Comments(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'parent_post')

class Friends(admin.ModelAdmin):
    list_display = ('id', 'requester', 'receiver', 'accepted')

class Users_Admin(admin.ModelAdmin):
    list_display = ('user', 'git_url', 'default_post_visibility', 'approved')

admin.site.register(Comment,Comments)
admin.site.register(Friend,Friends)
admin.site.register(Image)
admin.site.register(Post,Posts)
admin.site.register(Users,Users_Admin)
# Register your models here.
