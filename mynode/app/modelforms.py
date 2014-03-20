from django.db import models
from django import forms
from django.forms import ModelForm

from app.models import *

class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('author',)

class PostForm(ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    class Meta:
        model = Post
        exclude = ('author',)