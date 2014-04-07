from django.db import models
from django import forms
from django.forms import ModelForm
from app.models import *

attrs_dict = {'class': 'required'}

class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('author',)

class PostForm(ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':4}))
    class Meta:
        model = Post
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['recipient']=forms.ModelChoiceField(queryset=User.objects.exclude(id=user).exclude(is_superuser=1), required=False)
        self.fields['image']=forms.ModelChoiceField(queryset=Image.objects.filter(author=user), required=False)
