from django.db import models
from django import forms
from django.forms import ModelForm

from app.models import *

class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('author',)

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['recipient']=forms.ModelChoiceField(queryset=User.objects.exclude(id=user), required=False)
        self.fields['image']=forms.ModelChoiceField(queryset=Image.objects.filter(author=user), required=False)