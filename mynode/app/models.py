# This model is no longer auto-generated: run syncdb to sync database to these models
# Note: It will not alter tables that already exist, only create ones which do not

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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
        unique_together = ('requester','receiver')

class Image(models.Model):
    author = models.ForeignKey(User, db_column='author')
    image = models.ImageField(upload_to='images')
    visibility = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label='app'


class Post(models.Model):
    PUBLIC = 1
    SERVER = 2
    FRIENDS = 3
    PRIVATE = 4
    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (SERVER, 'Server'),
        (FRIENDS, 'Friends'),
        (PRIVATE, 'Private')
    )
    
    author = models.ForeignKey(User, related_name='author_user')
    recipient = models.ForeignKey(User, related_name='recipient_user', null=True)
    content = models.TextField(blank=True)
    content_type = models.IntegerField(blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True, choices=VISIBILITY_CHOICES)
    class Meta:
        app_label='app'
        

class Users(models.Model):
    git_url = models.CharField(max_length=256, blank=True)
    default_post_visibility = models.IntegerField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    user = models.OneToOneField(User, primary_key=True, parent_link=True)
    class Meta:
        app_label='app'

