from django.db import models
from django import forms
from django.forms import ModelForm
from app.models import *

attrs_dict = {'class': 'required'}

class ImageForm(ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'placeholder':'Image name'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'style':'padding-top=15px'}))
    visibility = forms.ChoiceField(choices=Image.VISIBILITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:150px;',}))
    class Meta:
        model = Image
        exclude = ('author',)

class PostForm(ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'placeholder':'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder':'Content...'}))
    visibility = forms.ChoiceField(choices=Post.VISIBILITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:150px;',}))
    content_type = forms.ChoiceField(choices=Post.CONTENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:150px;',}))

    class Meta:
        model = Post
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['recipient']=forms.ModelChoiceField(queryset=User.objects.exclude(id=user).exclude(is_superuser=1), required=False, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:150px;',}))
        self.fields['image']=forms.ModelChoiceField(queryset=Image.objects.filter(author=user), required=False, widget=forms.Select(attrs={'class': 'form-control', 'style':'width:150px;',}))

        
