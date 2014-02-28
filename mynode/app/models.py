# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=36)
    parent_post = models.ForeignKey('Post', db_column='parent_post')
    author = models.ForeignKey('Users', db_column='author')
    content = models.TextField(blank=True)
    class Meta:
        app_label='app'

class Friend(models.Model):
    request_id = models.CharField(primary_key=True, max_length=36)
    requester = models.ForeignKey('Users', db_column='requester', related_name='requester_userid')
    friend = models.ForeignKey('Users', db_column='friend', related_name='friend_userid')
    accepted = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label='app'


class Image(models.Model):
    image_id = models.CharField(primary_key=True, max_length=36)
    author = models.ForeignKey('Users', db_column='author')
    filename = models.CharField(max_length=128)
    visibility = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label='app'


class Post(models.Model):
    post_id = models.CharField(primary_key=True, max_length=36)
    author = models.ForeignKey('Users', db_column='author')
    content = models.TextField(blank=True)
    content_type = models.IntegerField(blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label='app'
        

class Users(models.Model):
    display_name = models.CharField(max_length=128)
    git_url = models.CharField(max_length=256, blank=True)
    default_post_visibility = models.IntegerField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, unique=True)
    class Meta:
        app_label='app'

