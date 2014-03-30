__author__ = 'Christian & Kris'
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
import sys

# Use http://jsonlint.com to validate JSON before commit

#GET/POST/PUT a post to the service API
@login_required
def post(request, post_id):
    context = RequestContext(request)
    if request.method == 'GET' or request.method == 'POST':
        try:
            #TODO Update the URI to access posts, have it use the posts uuid but in a nicer format
            #TODO Refactor fetching a posts JSON out of the request so it can be used to get all posts
            # Initialize some important object based on the request
            post = Post.objects.get(id = post_id)
            author = Users.objects.get(user_id=post.author)

            # Initialize the JSON containers
            response_json = []
            posts_json = {}
            post_author_json = {}
            comments_json = []
            return_json = {}

            # Filling out the post information
            post_author_json['id'] = author.uuid
            post_author_json['displayname'] = author.user.username
            #TODO: Fix this to properly reflect the host and author location
            post_author_json['url'] = "http://127.0.0.1:8000/service/author/" + author.uuid #TODO
            post_author_json['host'] = "http://127.0.0.1:8000" #TODO

            # Add the author to the post information
            posts_json['author'] = {}
            posts_json['author'] = post_author_json

            # Fill out the post information
            #TODO: Fix the TODO's in the JSON/below
            posts_json['title'] = post.title
            posts_json['source'] = "TODO" #TODO
            posts_json['origin'] = "TODO" #TODO
            posts_json['description'] = post.description
            posts_json['content'] = post.content
            posts_json['categories'] = {}
            posts_json['pubDate'] = str(post.post_date)
            posts_json['guid'] = post.uuid
            posts_json['visibility'] = 'TODO' #TODO
            content_type = post.content_type
            if content_type == 1:
                posts_json['content-type'] = 'text/plain'
            elif content_type == 2:
                posts_json['content-type'] = 'text/markdown'
            elif content_type == 3:
                posts_json['content-type'] = 'text/html'

            # Iterate through the comments and add them to the Comment JSON
            comment_set = Comment.objects.filter(parent_post = post_id)
            if comment_set:
                for comment in comment_set:
                    # Get the comment information
                    comment_json = {}
                    comment_json['comment'] = comment.content
                    comment_json['PubDate'] = str(comment.post_date)
                    comment_json['guid'] = comment.uuid

                    # Construct the comment author JSON
                    comment_json['author'] = {}
                    comment_author_json = {}
                    comment_author = Users.objects.get(user_id = comment.author)
                    comment_author_json['id'] = comment_author.uuid
                    comment_author_json['displayname'] = comment_author.user.username
                    comment_author_json['host'] = "http://127.0.0.1:8000 TODO" #TODO
                    comment_json['author'] = comment_author_json

                    # Add comment to comment array
                    comments_json.append(comment_json)

            # Combine the sub-elements into the response JSON
            posts_json['comments'] = comments_json
            response_json.append(posts_json)
            return_json['posts'] = response_json
            return HttpResponse(json.dumps(return_json), content_type="application/json")
        
        except:
            # Print the except for quiet errors once deployed, comment out the try & except when debugging
            e = sys.exc_info()[0]
            print(e)
            return HttpResponse(json.dumps("{}"), content_type="application/json")
    elif request.method == 'PUT':
        #TODO Here we should update the post information
        # We should create a post and return it using the json information here
        return HttpResponse(json.dumps("{}"), content_type="application/json")
    # If we somehow (not a get, post, or put) get here return empty json
    return HttpResponse(json.dumps("{}"), content_type="application/json", status = 405)


def friendship(request, uuidA, uuidB):
    context = RequestContext(request)
    if request.method == 'GET':

        return_json = {}
        return_json['query'] = "friends"

        #API example has friends listed twice, doesnt seem to work. maybe just a typo
        return_json['friends'] = uuidA, uuidB

        try:
            userA = Users.objects.get(uuid=uuidA)
            userB = Users.objects.get(uuid=uuidB)
            Friend.objects.get(requester=userA.user.id, receiver=userB.user.id, accepted=1)

        except:
            #either user not found or not friends
            return_json['friends'] = "NO"
            return HttpResponse(json.dumps(return_json), content_type="application/json")

        else:
            return_json['friends'] = "YES"
            return HttpResponse(json.dumps(return_json), content_type="application/json")

def friendshipList(request, authorUUID):
    context = RequestContext(request)
    if request.method == 'POST':

        return_json = {}
        return_json['query'] = request.POST['query']
        return_json['author'] = request.POST['author']

        vals = request.POST['authors']

        #TODO still need to return a proper list of friends
        print vals

        try:
            app_author = Users.objects.get(uuid=authorUUID)

        except:
            return_json['friends'] = []
            return HttpResponse(json.dumps(return_json), content_type="application/json")




        return HttpResponse(json.dumps(return_json), content_type="application/json")







