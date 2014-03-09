from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import *


def index(request):
    latest_posts = Posts.objects.all().order_by('date')[:50]
    #context = {'latest_posts_list': latest_posts_list}
    latest_posts = Posts.objects.all()
    context = RequestContext(request)
    return render_to_response ('stream_page.html', {'posts': latest_posts}, context)

def login(request):
    context = RequestContext(request)
    #TODO: if not logged in return login_page else return stream_page
    return render_to_response ('login_page.html', context)

def register(request):
    context = RequestContext(request)

    if request.method == 'GET':
        return render_to_response('registration_page.html', context)
    else:
        # A POST request @TODO: Validation, OR switch to forms
        form = request.POST # Bind data from request.POST into a PostForm
        user = User.objects.create_user(request.POST['username'],
                request.POST['email'],
                request.POST['pwd'])
        user.save()
        app_user = Users.objects.create(user = user)
        app_user.save()

        return render_to_response('stream_page.html', context)

def validateLogin(request):
    context = RequestContext(request)
    username = request.POST['username']
    pwd = request.POST['password']
    user = authenticate(username=username, password=pwd)

    #if user is not None:

     #   if user.is_active:
            #login(request,user)
            #temp redirect for testing
      #      return redirect ('stream_page.html', context)

       # else:
            #disabled account
   # else:
        #invalid login - tmp redirect for testing
    #    return redirect('friend_page.html', context)

#The stream contains posts, so although it doesn't look restful, it is.
@login_required
def stream(request):
    context = RequestContext(request)
    #TODO: narrow this down to show only allowed posts, not all posts
    current_user = Users.objects.get(user=request.user)
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
        return post_delete(request, post_id);
    if request.method == 'PUT':
        return post_put(request);


def delete_post(request, post_id):
    context = RequestContext(request)
    Post.objects.get(id=post_id).delete()
    return redirect('app.views.stream')

def create_post(request):
    current_user = Users.objects.get(user=request.user)
    context = RequestContext(request)
    post = Post.objects.create(author=current_user, content=request.POST['content']);
    post.save()
    #TODO: update post
    return redirect('app.views.stream')

def create_comment(request, parent_post):
    #the_post_lol = 
    current_user = Users.objects.get(user=request.user)
    # lol
    the_post_haha = Post.objects.get(id=parent_post)
    context = RequestContext(request)
    comment = Comment.objects.create(parent_post=the_post_haha, author=current_user, content=request.POST['content']);
    #post.save()
    #TODO: update post
    return redirect('app.views.stream')

@login_required
def friends(request):
    #TODO: friend stuff
    #friend_requests = FriendRequests.objects.get(user=request.user)
    followers = Friend.objects.all()
    following = Friend.objects.all()
    data = {'friend_requests':'request!', 'followers':followers, 'following':following}
    return render(request, 'friend_page.html', data)
