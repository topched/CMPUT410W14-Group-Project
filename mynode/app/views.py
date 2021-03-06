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

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from app.models import *
from app.modelforms import *
from django.conf import settings
import json
import urllib2
import datetime


#Simple Login View that uses the Django Auth Login System
def login(request):
    context = RequestContext(request)
    #TODO: if not logged in return login_page else return stream_page
    if request.user.is_authenticated():
        return redirect(stream)
    else:
        return HttpResponseRedirect('login/', context)

@login_required
def logout_view(request):
    context = RequestContext(request)
    logout(request)
    return HttpResponseRedirect('mynode/login/', context)

#Registration View
# GET: Returns the registration page
# POST: Creates a user with the parameters in the POST
# Note: Uses both the django User model and our Users model to extend it
# Must rename auth login function because login view
from django.contrib.auth import login as auth_login
def register(request):
    context = RequestContext(request)

    if request.method == 'GET':
        return render_to_response('registration_page.html', context)
    else:
        user = User.objects.create_user(username=request.POST['username'],
                                        email=request.POST['email'],
                                        password=request.POST['pwd'],
                                        first_name=request.POST['surname'],
                                        last_name=request.POST['lastname'])
        user.save()
        app_user = Users.objects.create(user=user, git_url=request.POST['git'])
        app_user.approved = False
        app_user.save()
        return redirect(login)
        # Login user if registration went okay.
        #auth_user = authenticate(username=request.POST['username'], password=request.POST['pwd'])
        #auth_login(request, auth_user)
        #if request.user.is_authenticated():
        #    return redirect(stream)

# Profile View for modifying your profile
# GET: Renders the profile page with the data from the logged in user
# POST: Updates any changed data for the user
@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def author_profile(request, author_id):
    context = RequestContext(request)

    author = User.objects.get(id=author_id)
    app_user = Users.objects.get(user_id=author.id)

    posts = Post.visible_posts.getAllVisibleByAuthor(request.user.id, author=author_id)
    
    # Sorts posts from newest to oldest
    posts.sort(key=lambda y: y.post_date, reverse=True)

    if request.method == 'GET':
        return render_to_response('author_profile_page.html', {'author': author, 'app_user': app_user, 'posts': posts}, context)

# Profile View for modifying your profile
# GET: Renders the profile page with the data from the logged in user
# POST: Updates any changed data for the user
@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def profile(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        auth_user = request.user

    user = User.objects.get(id=auth_user.id)
    app_user = Users.objects.get(user_id=auth_user.id)
    posts = Post.objects.filter(author=auth_user.id)

    if request.method == 'GET':
        return render_to_response('profile_page.html', {'user': user, 'app_user': app_user, 'posts': posts}, context)
    else:
        user.email = request.POST['email']
        user.set_password(request.POST['pwd'])
        user.first_name = request.POST['surname']
        user.last_name = request.POST['lastname']
        user.save()

        app_user.git_url = request.POST['git']
        app_user.avatar = request.POST['avatar-choice']
        app_user.save()

        return redirect('app.views.stream')


#The stream contains posts, so although it doesn't look restful, it is.
@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def stream(request):
    context = RequestContext(request)

    if Users.objects.get(user_id=request.user.id).approved == False:
        return render(request, 'wait.html')


    current_user = User.objects.get(id=request.user.id)
    app_user = Users.objects.get(user_id=current_user.id)
    
    posts = Post.visible_posts.getAllVisible(request.user.id)
    get_comments = Comment.objects.all()
    comments = []
    for comment_object in get_comments:
        comments.append(comment_object)

    #get the github json
    tmpUser = Users.objects.get(user_id=request.user.id)
    gitJson = github_feed(tmpUser.git_url)
    try:
        vals = json.loads(gitJson)

        #adding github posts
        if len(vals) > 0:
            display_count = 10
            if(len(vals) < display_count):
                display_count = len(vals) - 1

            #create a temp user for github posts
            gitUser = User()
            gitUser.username = "GitHub"
            gitUser.email = "temp@temp.com"
            gitUser.password = "password"
            gitUser.first_name = "git"
            gitUser.last_name = "user"

            #how many github entries to show in the stream -- Usually 100 results in vals
            for x in range(0, 10):
                gitItem = vals[x]
                #tmpUsername = gitItem['actor']['login']

                #handle a push event
                if gitItem['type'] == "PushEvent":
                    #itemContent = gitItem['payload']['commits']

                    post = Post()
                    post.author = gitUser
                    #pretty sure this number doesnt matter not actually a object for deletion
                    post.id = 999999

                    #post.content contains a html item
                    post.content = get_git_html_content(gitItem)

                    post.visibility = 1
                    #post content is html
                    post.content_type = 3
                    time = datetime.datetime.strptime(gitItem['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    post.post_date = time
                    post.description = "MYGITKEY-PushEvent"

                    post.title = gitItem['type']
                    posts.append(post)
    except:
        pass

    #get public posts from other servers
    servers = RemoteServers.objects.filter(active=True)
    remoteUser = User()
    remoteUser.username = "Remote User"
    remoteUser.first_name = "Remote"
    remoteUser.last_name = "User"
    for server in servers:

        remoteJson = get_remote_public_posts(server.hostname)
        if remoteJson is not None:

            val = json.loads(remoteJson)
            for x in range(0, len(val['posts'])):

                tmpPost = Post()
                remoteUser.username = val['posts'][x]['author']['displayname'] + " - " + val['posts'][x]['author']['host']
                tmpPost.author = remoteUser
                tmpPost.id = val['posts'][x]['guid']
                tmpPost.description = "MYREMOTEKEY"
                tmpPost.content = val['posts'][x]['content']
                tmpPost.post_date = datetime.datetime.strptime(val['posts'][x]['pubDate'], '%Y-%m-%d %H:%M:%S')
                contentType = val['posts'][x]['content-type']

                if contentType == "text/html":
                    tmpPost.content_type = 3
                if contentType == "text/x-markdown":
                    tmpPost.content_type = 2
                if contentType == "text/plain":
                    tmpPost.content_type = 1


                tmpComments = val['posts'][x]['comments']

                for y in range(0, len(tmpComments)):

                    tmpComment = Comment()
                    tmpComment.parent_post = tmpPost
                    tmpComment.author = remoteUser
                    tmpComment.content = tmpComments[y]['comment']
                    comments.append(tmpComment)

                posts.append(tmpPost)

    # Sorts posts from newest to oldest
    posts.sort(key=lambda y: y.post_date, reverse=True)

    #print comments
    data = {'posts': posts, 'comments': comments, 'current_user': current_user, 'app_user': app_user}
    return render_to_response('stream_page.html', data, context)

#returns a html content section for a github post
def get_git_html_content(gitItem):

    itemcontent = gitItem['payload']['commits']
    username = gitItem['actor']['login']

    #only gets the first commit message -- could return more then 1 here
    #TODO - create better content using more then the message
    author = itemcontent[0]['author']['name']
    authorurl = "https://github.com/" + username
    repo = gitItem['repo']['name']
    repourl = "https://github.com/" + repo
    commiturl = "https://github.com/" + gitItem['repo']['name'] + "/commit/" + itemcontent[0]['sha']

    eventhtml = "<a href=" + authorurl + ">" + author + "</a> Pushed To <a href=" \
        + repourl + ">" + repo + "</a></br></br>"

    messagehtml = itemcontent[0]['message'] + "</br></br>"
    commithtml = "View the full commit <a href=" + commiturl + ">Here</a>"

    content = eventhtml + messagehtml + commithtml

    return content

#Returns a json object of a specific users received events if the username is valid
def github_feed(username):

    #print username
    #events created url
    #urlEC = "https://api.github.com/users/ + username + /events"
    #reqEC = urllib2.Request(urlEC)

    #events received url
    url = "https://api.github.com/users/" + username + "/received_events"
    #print url
    req = urllib2.Request(url)

    try:
        resp = urllib2.urlopen(req)
        events = resp.read()
        return events
    except:
       pass

    return None

def get_remote_public_posts(hostname):

    url = hostname + "posts"

    try:
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        post = resp.read()
        return post
    except:
        return None


#Is this actually working?
@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def post_details(request, post_id):
    context = RequestContext(request)
    if request.method == 'DELETE' or request.POST.get('_method') == 'DELETE':
        return post_delete(request, post_id)
    if request.method == 'PUT':
        return post_put(request)

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def delete_post(request, post_id):
    context = RequestContext(request)
    Post.objects.get(id=post_id).delete()
    #TODO: Should delete all related COMMENTS as well
    return redirect('app.views.stream')

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def create_post(request, post_id=None):
    if request.method == 'GET':
        postForm = PostForm(user=request.user.id)

        return render(request, 'create_post.html', {'PostForm': postForm})
    else:
        current_user = User.objects.get(id=request.user.id)
        newPostForm = PostForm(request.POST, user=request.user.id)
        if (newPostForm.is_valid()):
            newPost = newPostForm.save(commit=False)
            newPost.author = current_user
            # This is all done when you pass the post data to the PostForm
            #newPost.title = request.POST['title']
            #newPost.content_type = request.POST['content-type']
            #newPost.visibility = request.POST['visibility']
            newPost.save()
            return HttpResponseRedirect('/mynode/stream')
        return render(request, 'create_post.html', {'PostForm': newPostForm})
    #TODO: update post
        return redirect('app.views.stream')

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def create_comment(request, parent_post):
    context = RequestContext(request)
    current_user = User.objects.get(id=request.user.id)
    the_post = Post.objects.get(id=parent_post)
    comment = Comment.objects.create(parent_post=the_post, author=current_user, content=request.POST['content'])
    #post.save()
    #TODO: update post
    return redirect('app.views.stream')

# Gets the friend page along with all friend data
# Followers = People who try to befriend you but you haven't accepted them yet
# Following = People who you are following but they haven't accepted you yet
# Friends = People who follow eachother
@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def friends(request):
    #TODO: friend stuff
    friend_requests = Friend.objects.filter(accepted = 0, receiver=request.user.id)
    followers = Friend.objects.filter(accepted = 2, receiver=request.user.id)
    following = Friend.objects.filter(requester=request.user.id).exclude(accepted = 1)
    friends = Friend.objects.filter(accepted = 1, requester=request.user.id)

    remote_followers = RemoteFriends.objects.filter(local_accepted=False, remote_accepted=True,blocked=False, local_receiver=request.user)
    remote_following = RemoteFriends.objects.filter(local_accepted=True, remote_accepted=False, local_receiver=request.user)
    remote_friends = RemoteFriends.objects.filter(local_accepted=True, remote_accepted=True, local_receiver=request.user)

    user = User.objects.get(id=request.user.id)

    data = {'friend_requests': friend_requests, 'followers': followers, 'following': following, 'friends': friends,
            'user': user, 'remote_follower':remote_followers, 'remote_following':remote_following, 'remote_friends':remote_friends}
    return render(request, 'friend_page.html', data)

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def create_friend(request):
    #@TODO Check if this will make them friends
    current_user = User.objects.get(id=request.user.id)
    receiver_name = request.POST['receiver_display_name']
    print receiver_name

    #TODO: Fancy up the "Person does not exists" code.
    try:
        receiver = User.objects.get(username=receiver_name)
    except User.DoesNotExist:
        return redirect('app.views.friends')

    #try:
    friend = Friend.objects.create(receiver=receiver, requester=current_user)
    friend.save()
    #except IntegrityError:
    #    friendship = Friend.objects.get(requester=current_user, receiver=receiver_name)
    #    friendship.accepted = 0
    #    return redirect('app.views.friends')
    return redirect('app.views.friends')

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def deny_friend(request, follower_id):
    current_user = User.objects.get(id=request.user.id)
    sender = User.objects.get(id=follower_id)
    friendship = Friend.objects.get(requester=sender, receiver=current_user)
    # TODO: This should actually delete the relationship, not update it.
    # Should only be able to delete your own relationships.
    #friendship = Friend.objects.get(requester=current_user, receiver=sender)
    #friendship.delete();

    # Apparently we changed this from bool to int, with 2 meaning the friendship
    # was denied.
    friendship.accepted = 2
    friendship.save()
    return redirect('app.views.friends')

# Accepting a friend request sent to you
# If you are already following them it will make you friends
# If you are not following them it will follow them and make you friends
@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def confirm_friend(request, follower_id):
    current_user = User.objects.get(id=request.user.id)
    sender = User.objects.get(id=follower_id)
    friendship = Friend.objects.get(requester=sender, receiver=current_user)

    try:
        friendship2 = Friend.objects.get(requester=current_user, receiver=sender)
    except:
        friendship2 = Friend.objects.create(requester=current_user, receiver=sender, accepted=1)
    friendship.accepted = 1
    friendship.save()
    friendship2.accepted = 1
    friendship2.save()

    return redirect('app.views.friends')

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def delete_friend(request, receiver_id):
    current_user = User.objects.get(id=request.user.id)
    receiver = User.objects.get(id=receiver_id)
    # Delete users half of the friendship
    friendship = Friend.objects.get(requester=current_user, receiver=receiver)
    friendship.delete()

    # Set other half of friendship to 'denied', if it exists
    try:
        friendship2 = Friend.objects.get(requester=receiver, receiver=current_user)
        friendship2.accepted = 2
        friendship2.save()
    except:
        return redirect('app.views.friends')

    return redirect('app.views.friends')

@login_required
@user_passes_test(lambda u: Users.objects.get(user_id=u.id).approved, login_url='/mynode/approval_needed')
def image(request, image_id=None):
    if request.method == 'GET':
        if (image_id is None):
            imageForm = ImageForm()
            return render(request, 'image_upload.html', {'ImageForm': imageForm})
        else:
            print request.user
            img = Image.visibile_images.get(image_id, request.user.id)
            if(img is not None):
                return render(request, 'view_image.html', {'Image': img})
            else:
                raise PermissionDenied
    elif request.method == 'POST':
        newImageForm = ImageForm(request.POST, request.FILES)
        if (newImageForm.is_valid()):
            newImage = newImageForm.save(commit=False)
            newImage.author = request.user
            newImage.save()
            return redirect('app.views.stream')
        return render(request, 'image_upload.html', {'ImageForm': newImageForm})
    elif request.method == "DELETE":
        Post.objects.get(id=image_id).delete()
        return redirect('app.views.stream')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def approval_needed(request):
    return render(request, 'wait.html')

def user_approved(user):
    app_user = Users.objects.get(user_id=user.id)
    return app_user.approved
