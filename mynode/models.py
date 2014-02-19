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

class Comments(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=36)
    parent_post = models.ForeignKey('Posts', db_column='parent_post')
    author = models.ForeignKey('Users', db_column='author')
    content = models.TextField(blank=True)
    comment_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'comments'

class Friends(models.Model):
    request_id = models.CharField(primary_key=True, max_length=36)
    requester = models.ForeignKey('Users', db_column='requester')
    friend = models.ForeignKey('Users', db_column='friend')
    accepted = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'friends'

class Images(models.Model):
    image_id = models.CharField(primary_key=True, max_length=36)
    author = models.ForeignKey('Users', db_column='author')
    filename = models.CharField(max_length=128)
    visibility = models.IntegerField(blank=True, null=True)
    image_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'images'

class Posts(models.Model):
    post_id = models.CharField(primary_key=True, max_length=36)
    author = models.ForeignKey('Users', db_column='author')
    image = models.ForeignKey(Images, blank=True, null=True)
    content = models.TextField(blank=True)
    content_type = models.IntegerField(blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)
    post_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'posts'

class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=36)
    display_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    git_url = models.CharField(max_length=256, blank=True)
    email = models.CharField(max_length=256)
    default_post_visibility = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'users'

