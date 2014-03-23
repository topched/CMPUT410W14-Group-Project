__author__ = 'Christian'
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from app.models import *
from django.core import serializers
import json

#GET/POST/PUT a post to the service API
@login_required
def post(request, post_id):
    context = RequestContext(request)
    if request.method == 'GET' or request.method == 'POST':
        try:
            post = Post.objects.get(id = post_id)
            author = post.author
            comments = Comment.objects.filter(parent_post = post)

            return HttpResponse(serializers.serialize("json",comments), content_type="application/json")
        except:
            return HttpResponse(json.dumps("{}"), content_type="application/json")
    elif request.method == 'POST':
        # We should create a post and return it using the json information here
        return HttpResponse(json.dumps("{}"), content_type="application/json")
    # If we somehow get here return empty json
    return HttpResponse(json.dumps("{}"), content_type="application/json")