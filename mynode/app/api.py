#    Copyright 2014 Christian Jukna, Erin Torbiak, Jordan Ching, Kris Kushniruk
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
__author__ = 'Christian & Kris'
import json
import sys
import urllib2
import requests
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.models import User
from app.models import *
from django.conf import settings


# Use http://jsonlint.com to validate JSON before commit
# FROM JSON sample on hindles github
# The following are ways URIs that can be used for post retrieval
#
# http://service/author/posts (posts that are visible to the currently authenticated user)
# or
# http://service/posts (all posts marked as public on the server)
# or
# http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
# or
# http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
#
# All of the previous URIs will get a list of posts like this:

def get_post(post_id):
    # Initialize some important object based on the request
    post = Post.objects.get(id=post_id)
    author = Users.objects.get(user_id=post.author)

    # Initialize the JSON containers
    posts_json = {}
    post_author_json = {}
    comments_json = []

    # Filling out the post information
    post_author_json['id'] = author.uuid
    post_author_json['displayname'] = author.user.username
    post_author_json['url'] = "http://cs410.cs.ualberta.ca:41068/mynode/author/" + author.uuid
    post_author_json['host'] = "http://cs410-06/"

    # Add the author to the post information
    posts_json['author'] = {}
    posts_json['author'] = post_author_json

    # Fill out the post information
    #TODO: Fix the TODO's in the JSON/below
    posts_json['title'] = post.title
    posts_json['source'] = "http://cs410.cs.ualberta.ca:41068/" #TODO
    posts_json['origin'] = "http://cs410.cs.ualberta.ca:41068/" #TODO
    posts_json['description'] = post.description
    posts_json['content'] = post.content
    posts_json['categories'] = {}
    posts_json['pubDate'] = str(post.post_date)
    posts_json['guid'] = post.uuid
    visibility = post.visibility
    if visibility == 1:	
    	posts_json['visibility'] = 'PUBLIC'
    elif visibility == 2:
	posts_json['visibility'] = 'SERVERONLY'
    elif visibility == 3:
	posts_json['visibility'] = 'FOAF'
    elif visibility == 4:
	posts_json['visibility'] = 'FRIENDS'
    elif visibility == 5:
	posts_json['visibility'] = 'PRIVATE'

    content_type = post.content_type
    if content_type == 1:
        posts_json['content-type'] = 'text/plain'
    elif content_type == 2:
        posts_json['content-type'] = 'text/x-markdown'
    elif content_type == 3:
        posts_json['content-type'] = 'text/html'

    # Iterate through the comments and add them to the Comment JSON
    comment_set = Comment.objects.filter(parent_post=post_id)
    if comment_set:
        for comment in comment_set:
            # Get the comment information
            comment_json = {}
            comment_json['comment'] = comment.content
            comment_json['pubDate'] = str(comment.post_date)
            comment_json['guid'] = comment.uuid

            # Construct the comment author JSON
            comment_json['author'] = {}
            comment_author_json = {}
            comment_author = Users.objects.get(user_id=comment.author)
            comment_author_json['id'] = comment_author.uuid
            comment_author_json['displayname'] = comment_author.user.username
            comment_author_json['host'] = "http://cs410-06/" #TODO
            comment_json['author'] = comment_author_json

            # Add comment to comment array
            comments_json.append(comment_json)

    # Combine the sub-elements into the response JSON
    posts_json['comments'] = comments_json

    return posts_json

#GET/POST/PUT a post to the service API
@login_required
def post(request, post_uuid):
    temp_post = Post.objects.get(uuid=post_uuid)
    post_id = temp_post.id
    if request.method == 'GET' or request.method == 'POST':
        try:
            response_json = []
            return_json = {}
            response_json.append(get_post(post_id))
            return_json['posts'] = response_json
            return HttpResponse(json.dumps(return_json), content_type="application/json")
        except:
            # Print the except for quiet errors once deployed, comment out the try & except when debugging
            e = sys.exc_info()[0]
            print(e)
            return HttpResponse(json.dumps("{}"), content_type="application/json")
    elif request.method == 'PUT':
        #TODO Here we should update the post information
        #TODO Is this actually necessary? I'm not sure
        # We should create a post and return it using the json information here
        post_json = json.loads(request.body)

        post = Post.objects.get(id=post_id)
        try:
            post.content = post_json['content']
        except:
            pass


        post.save()
        return HttpResponse(json.dumps("{}"), content_type="application/json")
        # If we somehow (not a get, post, or put) get here return empty json
    return HttpResponse(json.dumps("{}"), content_type="application/json", status=405)

# Get all the public posts on the server along with their comments
def posts(request):
    if request.method == 'GET':
        response_json = []
        return_json = {}
        # Only public posts
        post_set = Post.objects.filter(visibility=1)
        # For each post create the JSON object
        if post_set:
            for post in post_set:
                # Add the post JSON to the response set
                response_json.append(get_post(post.id))
        return_json['posts'] = response_json
        return HttpResponse(json.dumps(return_json), content_type="application/json")
    elif request.method == 'PUT':
        #TODO Here we should post based on the JSON being passed
        # We should create a post and return it using the json information here
        post_json = json.loads(request.DATA)
        return HttpResponse(json.dumps("{}"), content_type="application/json")
    # Anything other than GET returns a 403
    return HttpResponse(status=403)

# Get all the posts visible to the current authenticated user
@csrf_exempt
def author_posts(request):
    if request.method == 'GET':
        try:
	    remote_uuid = request.GET['id']
	except: 
	    return HttpResponse(status=403)
	response_json = []
        return_json = {}
        # Only posts visible for this user
        post_set = Post.visible_posts.getAllVisibleRemote(remote_uuid)
        # For each post create the JSON object
        if post_set:
            for post in post_set:
                # Add the post JSON to the response set
                response_json.append(get_post(post.id))
        return_json['posts'] = response_json
        return HttpResponse(json.dumps(return_json), content_type="application/json")
    # Anything other than GET returns a 403
    return HttpResponse(status=403)

# Get all the posts visible to the current authenticated user for a specific author
@csrf_exempt
def specific_author_posts(request, author_id):
    if request.method == 'GET':
        try:
	    remote_uuid = request.GET['id']
	except:
	    return HttpResponse(status=403)
	
	response_json = []
        return_json = {}
        # Only posts visible for this user
        post_set = Post.visible_posts.getAllVisibleRemote(remote_uuid)
        # For each post create the JSON object
        if post_set:
            for post in post_set:
                # Add the post JSON to the response set if it is from the author we want
                if post.author == User.objects.get(id=author_id):
                    response_json.append(get_post(post.id))
        return_json['posts'] = response_json
        return HttpResponse(json.dumps(return_json), content_type="application/json")
    # Anything other than GET returns a 403
    return HttpResponse(status=403)

# a response if friends or not -- ask the service htt://service/friends/<uuidA>/<uuidB>
# responds with JSON
#   {"query: "friends",
#    "friends": [uuidA, uuidB],
#    "friends": YES or NO }
#TODO - friends listed twice -- deal with this
@csrf_exempt
def friendship(request, uuidA, uuidB):
    context = RequestContext(request)
    if request.method == 'GET':

        return_json = {}
        return_json['query'] = "friends"

        #API example has friends listed twice, doesnt seem to work. maybe just a typo
        return_json['friends'] = [uuidA, uuidB]

        try:
            userA = Users.objects.get(uuid=uuidA)
            RemoteFriends.objects.get(uuid=uuidB, local_receiver=userA.user, local_accepted=True, remote_accepted=True)
        except:
            pass
             
        try:
            userB = Users.objects.get(uuid=uuidB)
            RemoteFriends.objects.get(uuid=uuidA, local_receiver=userB.user, local_accepted=True, remote_accepted=True)
        except:
            pass        	
        
        try:
            userA = Users.objects.get(uuid=uuidA)
            userB = Users.objects.get(uuid=uuidB)
            Friend.objects.get(requester=userA.user.id, receiver=userB.user.id, accepted=1)
       
        except Users.DoesNotExist:
            return_json['friends'] = "NO USER"
            return HttpResponse(json.dumps(return_json), content_type="application/json") 

        except Friend.DoesNotExist:
            return_json['friends'] = "NO Friend"
            return HttpResponse(json.dumps(return_json), content_type="application/json")



        else:
            return_json['friends'] = "YES"
            return HttpResponse(json.dumps(return_json), content_type="application/json") 

    else:
        return HttpResponse(405)




# anyone in the list a friend? POST to http://service/friends/authorUUID w/ a JSON object containing a list of UUID's
# responds with JSON
#   {"query": "friends",
#    "author": authorUUID,
#    "friends": [list containing the UUID's of all friends in the list] }
@csrf_exempt
def friendshipList(request, authorUUID):
    context = RequestContext(request)
    if request.method == 'POST':

        vals = json.loads(request.body)
        return_json = {}
        return_json['query'] = vals['query']
        return_json['author'] = vals['author']

        authors = []
        authors = vals['authors']

        friends = []
        try:
            for author in authors:
                try:

                    tmp = Users.objects.get(uuid=author)
                    tmp_user = tmp.user
                    #print tmp_user.id
                    #print authorUUID
                    friend = RemoteFriends.objects.get(uuid=vals['author'], local_receiver=tmp_user, local_accepted=True, remote_accepted=True)

                    if friend:
                        friends.append(author)
                except:
                    pass

        except:

            #either not a valid author or no friends matched
            return_json['friends'] = []
            return HttpResponse(json.dumps(return_json), content_type="application/json")

        else:
            return_json['friends'] = friends
            return HttpResponse(json.dumps(return_json), content_type="application/json")

    else:
        return HttpResponse(405)

# Add a remote friend request to our DB
@csrf_exempt
def friendrequest(request):
    if request.method == 'POST':
        vals = json.loads(request.body)
        try:
            remote_friend = RemoteFriends.objects.create(
                uuid=vals['author']['id'],
                displayname=vals['author']['displayname'],
                host=vals['author']['host'],
                remote_accepted=True,
                local_accepted=False,
                local_receiver=(Users.objects.get(uuid=vals['friend']['author']['id'])).user)
            remote_friend.save()
            return HttpResponse()
        except:
            try:
                remote_friend = RemoteFriends.objects.get(uuid=vals['author']['id'],
                                             local_receiver=(Users.objects.get(uuid=vals['friend']['author']['id'])).user)
                remote_friend.remote_accepted = True
                remote_friend.save()
                return HttpResponse()
            except:
                return HttpResponse(status=409)

    return HttpResponse(status=403)

@login_required
def delete_remote_friend(request, uuid):
    try:
        remote_request = RemoteFriends.objects.get(uuid=uuid, local_receiver=request.user)
        remote_request.blocked = True
        remote_request.save()
        return redirect('app.views.friends')
    except:
        # Do something here
        return redirect('app.views.friends')

@login_required
def confirm_remote_friend(request, uuid):
    #try:
        # Accept the friend request
        remote_request = RemoteFriends.objects.get(uuid=uuid, local_receiver=request.user)


        # Send out the JSON to their servers API to confirm
        data = {}
        author = {}
        friend = {}
        friend_author = {}
        data['query'] = "friendrequest"

        author['id'] = (Users.objects.get(user_id=request.user.id)).uuid
        author['host'] = 'http://cs410-06/'
        author['displayname'] = (User.objects.get(id=request.user.id)).username

        friend_author['id'] = remote_request.uuid
        friend_author['host'] = remote_request.host
        friend_author['displayname'] = remote_request.displayname
        friend_author['url'] = remote_request.host + "author/" + remote_request.uuid
        friend['author'] = friend_author
        data['author'] = author
        data['friend'] = friend

	#import os
	#os.environ['http_proxy']=''
	url_request = remote_request.host + "friendrequest"
        #url_request = "http://cs410.ualberta.ca:41078/friendrequest"
	print url_request
	#req = urllib2.Request(url_request)
        #req = urllib2.Request("http://127.0.0.1:8001/service/friendrequest")
#        req.add_header('Content-Type', 'application/json')
	headers = {'Content-Type':'application/json'}
	r = requests.post(url_request,data=json.dumps(data),headers=headers)
#	try:
#		response = urllib2.urlopen(req)#,# json.dumps(data), 5)
#	except urllib2.HTTPError, e:
#    		print(str(e.code))
#		return HttpResponse(json.dumps(data),content_type="application/json")
#	except urllib2.URLError, e:
#    		print(str(e.reason))
#		return HttpResponse(json.dumps(data),content_type="application/json")
#	except:
#		print("OH SHIT")
#		pass
 
        if r.status_code == 200 or r.status_code ==201:
             remote_request.local_accepted = True
             remote_request.save()

#	headers = {'Content-Type':'application/json'}
#	r = requests.get(url_request,data=json.dumps(data),headers=headers)
#	print r.response

#        return HttpResponse(json.dumps(data), content_type="application/json")
        return redirect('app.views.friends')
    #except:
    #    # Do something here
    #    return redirect('app.views.friends')

# Get a list of all our authors
def get_all_users(request):
	if (request.method == 'GET'):
		authors = Users.objects.filter()
		author_array = []
		for author in authors:
			author_json = {}
			author_json['displayname']=author.user.username
			author_json['id']=author.uuid
			author_array.append(author_json)
		return HttpResponse(json.dumps(author_array), content_type="application/json")
	else:
		return HttpResponse(409)
	
