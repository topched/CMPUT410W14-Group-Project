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
from django.forms import ModelForm
#from app.modelforms import *


def index(request):
    latest_posts = Posts.objects.all().order_by('date')[:50]
    #context = {'latest_posts_list': latest_posts_list}
    latest_posts = Posts.objects.all()
    context = RequestContext(request)
    return render_to_response ('stream_page.html', {'posts': latest_posts}, context)

#Simple Login View that uses the Django Auth Login System
def login(request):
    context = RequestContext(request)
    #TODO: if not logged in return login_page else return stream_page
    return render_to_response ('login_page.html', context)

#Registration View
# GET: Returns the registration page
# POST: Creates a user with the parameters in the POST
# Note: Uses both the django User model and our Users model to extend it
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
        app_user = Users.objects.create(user = user, git_url=request.POST['git'])
        app_user.save()

        return HttpResponseRedirect("/")

# Profile View for modifying your profile
# GET: Renders the profile page with the data from the logged in user
# POST: Updates any changed data for the user
@login_required
def profile(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        auth_user = request.user

    user = User.objects.get(id=auth_user.id)
    app_user = Users.objects.get(user_id=auth_user.id)

    if request.method == 'GET':
        return render_to_response('profile_page.html',{'user': user, 'app_user':app_user}, context)
    else:
        user.email = request.POST['email']
        user.set_password(request.POST['pwd'])
        user.first_name = request.POST['surname']
        user.last_name = request.POST['lastname']
        user.save()

        app_user.git_url = request.POST['git']
        app_user.save()

        return redirect('app.views.stream')


#The stream contains posts, so although it doesn't look restful, it is.
@login_required
def stream(request):
    context = RequestContext(request)
    #TODO: narrow this down to show only allowed posts, not all posts
    current_user = User.objects.get(id=request.user.id)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    print comments
    data = {'posts':posts, 'comments':comments, 'current_user':current_user}
    return render_to_response('stream_page.html', data, context)

def post_details(request, post_id):
    context = RequestContext(request)
    #if request.method == 'POST':
        # deletin
        # post.edeskajhdfasf
    if request.method == 'DELETE' or request.POST.get('_method') == 'DELETE':
        return post_delete(request, post_id)
    if request.method == 'PUT':
        return post_put(request)


def delete_post(request, post_id):
    context = RequestContext(request)
    Post.objects.get(id=post_id).delete()
    #TODO: Should delete all related COMMENTS as well
    return redirect('app.views.stream')

def create_post(request):
    current_user = User.objects.get(id=request.user.id)
    context = RequestContext(request)
    post = Post.objects.create(author=current_user, content=request.POST['content'])
    post.save()
    #TODO: update post
    return redirect('app.views.stream')

def create_comment(request, parent_post):
    #the_post_lol = 
    current_user = User.objects.get(id=request.user.id)
    # lol
    the_post_haha = Post.objects.get(id=parent_post)
    context = RequestContext(request)
    comment = Comment.objects.create(parent_post=the_post_haha, author=current_user, content=request.POST['content'])
    #post.save()
    #TODO: update post
    return redirect('app.views.stream')

# Gets the friend page along with all friend data
# Followers = People who try to befriend you but you haven't accepted them yet
# Following = People who you are following but they haven't accepted you yet
# Friends = People who follow eachother
@login_required
def friends(request):
    #TODO: friend stuff
    #friend_requests = FriendRequests.objects.get(user=request.user)
    followers = Friend.objects.filter(accepted=0,receiver=request.user.id)
    following = Friend.objects.filter(requester=request.user.id).exclude(accepted=1)
    friends = Friend.objects.filter(accepted=1,receiver=request.user.id)
    data = {'friend_requests':'request!', 'followers':followers, 'following':following, 'friends':friends}
    return render(request, 'friend_page.html', data)

# Not accepting a friend request that is sent to you
@login_required
def delete_friend(request, follower_id):
    current_user = User.objects.get(id=request.user.id)
    sender = User.objects.get(id=follower_id)
    friendship = Friend.objects.get(requester=sender,receiver=current_user)

    friendship.accepted = 2
    friendship.save()

    return redirect('app.views.friends')

# Accepting a friend request sent to you
# If you are already following them it will make you friends
# If you are not following them it will follow them and make you friends
@login_required   
def confirm_friend(request, follower_id):
    current_user = User.objects.get(id=request.user.id)
    sender = User.objects.get(id=follower_id)
    friendship = Friend.objects.get(requester=sender,receiver=current_user)
    
    try: friendship2 = Friend.objects.get(requester=current_user,receiver=sender)
    except: friendship2 = Friend.objects.create(requester=current_user,receiver=sender,accepted=1)
    friendship.accepted = 1
    friendship.save()
    friendship2.accepted = 1
    friendship2.save()
    
    return redirect('app.views.friends')
        
        
# Adds a friend by username
@login_required
def create_friend(request):
    #@TODO Check if this will make them friends
    current_user = User.objects.get(id=request.user.id)
    receiver_name = request.POST['receiver_display_name']
    print receiver_name

    #TODO: Fancy up the "Person does not exists" code.
    try : receiver = User.objects.get(username=receiver_name)
    except User.DoesNotExist: return redirect('app.views.friends')
    print "FRIEND CREATED"

    friend = Friend.objects.create(receiver=receiver, requester=current_user)
    friend.save()
    return redirect('app.views.friends')

def image(request, image_id=None):
    if request.method == 'GET':
        if(image_id is None):
            imageForm = ImageForm()
            return render(request,'image_upload.html', {'ImageForm':imageForm})
        else:
            return render(request,'view_image.html', {'Image':Image.objects.get(id=image_id)})
    elif request.method == 'POST':
        newImageForm = ImageForm(request.POST, request.FILES)
        if(newImageForm.is_valid()):
            newImage = newImageForm.save(commit=False)
            newImage.author = request.user
            newImage.save()
            return redirect('app.views.stream')
        return render(request, 'image_upload.html', {'ImageForm':newImageForm})
    elif request.method == "DELETE":
        Post.objects.get(id=image_id).delete()
        return redirect('app.views.stream')
    else:
        return HttpResponseNotAllowed(['GET','POST'])
        
