from django.db import models
from django.forms import ModelForm

from app.models import *

class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('author',)

#class PostForm(ModelForm):
#    class Meta:
#        model = Post
#        exclude = ('author',)

class Permissions():
    def canSeePost(self, post_id, requester):
        post = Post.objects.get(id=post_id)
        
        if(post.recipient == requester):
            return True
        elif(self.authLevel(post.author, requester) >= post.visibility):
            return True
        else:
            return False
    
    def canSeeImage(self, image_id, requester):
        image = Image.objects.get(id=image_id)
        
        if(self.authLevel(image.author, requester) >= image.visibility):
            return True
        else:
            return False
    
    def authLevel(self, owner, requester):
        if( owner == requester ):
            return Post.PRIVATE
        elif(self.areFriends(user1, user2)):
            return Post.FRIENDS
        elif(User.objects.get(id=requester)):
            return Post.SERVER
        else:
            return Post.PUBLIC
        
    def areFriends( self, user1, user2 ):
        if (not Friend.objects.get(requester=user1, receiver=user2, accepted=True) is None):
            return True
        elif(not Friend.objects.get(requester=user2, receiver=user1, accepted=True) is None):
            return True
        else:
            return False
