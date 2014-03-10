# This model is no longer auto-generated: run syncdb to sync database to these models
# Note: It will not alter tables that already exist, only create ones which do not

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    parent_post = models.ForeignKey('Post', db_column='parent_post')
    author = models.ForeignKey(User, db_column='author')
    content = models.TextField(blank=True)
    class Meta:
        app_label='app'

class Friend(models.Model):
    requester = models.ForeignKey(User, db_column='requester', related_name='requester_userid')
    receiver = models.ForeignKey(User, db_column='receiver', related_name='receiver_userid')
    accepted = models.IntegerField(default=False)
    class Meta:
        app_label='app'

class Image(models.Model):
    author = models.ForeignKey(User, db_column='author')
    filename = models.CharField(max_length=128)
    visibility = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label='app'


class Post(models.Model):
    author = models.ForeignKey(User, db_column='author')
    content = models.TextField(blank=True)
    content_type = models.IntegerField(blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label='app'
        

class Users(models.Model):
    git_url = models.CharField(max_length=256, blank=True)
    default_post_visibility = models.IntegerField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    user = models.OneToOneField(User, primary_key=True, parent_link=True)
    class Meta:
        app_label='app'

