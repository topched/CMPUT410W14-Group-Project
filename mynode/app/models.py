# This model is no longer auto-generated: run syncdb to sync database to these models
# Note: It will not alter tables that already exist, only create ones which do not

from __future__ import unicode_literals

from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField
from PIL import Image

    ##############
    #  MANAGERS  #
    ##############

class PostManager(models.Manager):
    def getAllVisible(self, requester):
        posts = super(PostManager, self).get_queryset().values_list('id',flat=True)
        visiblePosts = list()
        
        permissionHelper = Permissions()
        
        for post_id in posts:
            post = permissionHelper.canSeePost(post_id, requester)
            if(post is not None):
                visiblePosts.append(post)
        
        return visiblePosts

class ImageManager(models.Manager):
    def getAllVisible(self, requester):
        images = super(ImageManager, self).get_queryset().values_list('id',flat=True)
        visibleImages = list()
        
        permissionHelper = Permissions()
        
        for image_id in images:
            image = permissionHelper.canSeeImage(image_id, requester)
            if(image is not None):
                visibleImages.append(image)
        
        return visibleImages
    
    ############
    #  MODELS  #
    ############

class Comment(models.Model):
    parent_post = models.ForeignKey('Post', db_column='parent_post')
    author = models.ForeignKey(User, db_column='author')
    content = models.TextField(blank=True)
    uuid = UUIDField(version=4, unique=True)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'app'

class RemoteServers(models.Model):
    hostname = models.TextField(blank=True)
    active = models.IntegerField(default=False)

    class Meta:
        app_label = 'app'


class Friend(models.Model):
    requester = models.ForeignKey(User, db_column='requester', related_name='requester_userid')
    receiver = models.ForeignKey(User, db_column='receiver', related_name='receiver_userid')
    accepted = models.IntegerField(default=False)

    class Meta:
        app_label = 'app'
        unique_together = ('requester', 'receiver')


class Image(models.Model):
    PUBLIC = 1
    SERVER = 2
    FRIENDOF = 3
    FRIENDS = 4
    PRIVATE = 5
    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (SERVER, 'Server'),
        (FRIENDOF, 'Friends of Friends'),
        (FRIENDS, 'Friends'),
        (PRIVATE, 'Private')
    )
    
    author = models.ForeignKey(User, db_column='author')
    image = models.ImageField(upload_to='images')
    name = models.CharField(blank=False, null=False, max_length=256)
    visibility = models.IntegerField(blank=True, null=True, choices=VISIBILITY_CHOICES)

    class Meta:
        app_label = 'app'
    
    def __unicode__(self):
        return self.name


class Post(models.Model):
    PUBLIC = 1
    SERVER = 2
    FRIENDOF = 3
    FRIENDS = 4
    PRIVATE = 5
    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (SERVER, 'Server'),
        (FRIENDOF, 'Friends of Friends'),
        (FRIENDS, 'Friends'),
        (PRIVATE, 'Private')
    )
    
    PLAINTEXT = 1
    MARKDOWN = 2
    HTML = 3
    CONTENT_CHOICES = (
        (PLAINTEXT, 'Plaintext'),
        (MARKDOWN, 'Markdown'),
        (HTML, 'HTML')
    )
    
    author = models.ForeignKey(User, related_name='author_user')
    recipient = models.ForeignKey(User, related_name='recipient_user', null=True)
    image = models.ForeignKey(Image, null=True)
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    content_type = models.IntegerField(blank=True, null=True, choices=CONTENT_CHOICES)
    visibility = models.IntegerField(blank=True, null=True, choices=VISIBILITY_CHOICES)
    uuid = UUIDField(version=4, unique=True)
    post_date = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    visible_posts = PostManager()
    class Meta:
        app_label='app'
        

class Users(models.Model):
    git_url = models.CharField(max_length=256, blank=True)
    default_post_visibility = models.IntegerField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    user = models.OneToOneField(User, primary_key=True, parent_link=True)
    uuid = UUIDField(version=4, unique=True)
    class Meta:
        app_label='app'

class RemoteFriends(models.Model):
    uuid = models.CharField(max_length=256, blank=True)
    displayname = models.CharField(max_length=256, blank=True)
    host = models.CharField(max_length=256, blank=True)
    remote_accepted = models.IntegerField(default=False)
    local_accepted = models.IntegerField(default=False)
    local_receiver = models.ForeignKey(User, db_column='local_receiver', related_name='local_receiver')
    blocked = models.IntegerField(default=False)
    class Meta:
        app_label='app'
        unique_together = ('uuid', 'local_receiver')

class Permissions():
    def canSeePost(self, post_id, requester):
        post = Post.objects.get(id=post_id)
        if(post.recipient is not None):
            if(post.recipient.id == requester or post.author.id == requester):
                return post
            else:
                return None
        elif(self.authLevel(post.author.id, requester) >= post.visibility):
            return post
        else:
            return None
    
    def canSeeImage(self, image_id, requester):
        image = Image.objects.get(id=image_id)
        
        if(self.authLevel(image.author, requester) >= image.visibility):
            return image
        else:
            return None
    
    def authLevel(self, owner, requester):
        if( owner == requester ):
            return Post.PRIVATE
        elif(self.areFriends(owner, requester)):
            return Post.FRIENDS
        elif(self.isFriendOfFriend(owner, requester)):
            return Post.FRIENDOF
        else:
            try:
                User.objects.get(id=requester)
                return Post.SERVER
            except User.DoesNotExist:
                return Post.PUBLIC
        
    def areFriends( self, user1, user2 ):
        try:
            Friend.objects.get(requester=user1, receiver=user2, accepted=True)
            return True
        except Friend.DoesNotExist:
            return False
        
    def isFriendOfFriend(self, user1, user2):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM app_friend AS f1, app_friend AS f2 WHERE f1.accepted = 1 AND f2.accepted = 1 AND f1.requester = %s AND f2.requester = %s AND f1.receiver = f2.receiver LIMIT 1;", [user1, user2])
        result = cursor.fetchall()
        
        if(len(result) is not 0):
            return True
        else:
            return False
