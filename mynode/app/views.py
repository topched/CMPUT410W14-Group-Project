from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from app.models import *


def index(request):
    #latest_posts = Posts.objects.all().order_by('date')[:10]
    #context = {'latest_posts_list': latest_posts_list}
    latest_posts = Posts.objects.all()
    context = RequestContext(request)
    return render_to_response ('stream_page.html', {'posts': latest_posts}, context)
    
    
def login(request):
    context = RequestContext(request)
	
	#TODO: if not logged in return login_page else return stream_page
    return render_to_response ('login_page.html', context)
	


# Proper response once models are working.
# def friends(request):
#       friends = Friends.objects.all()
#       context = {'friends': friends}
#       return render(request, './friends.html', context)


def stream(request, template_name):
	context = RequestContext(request)
	return render_to_response('stream_page.html', context)
	
	
def friends(request, template_name):
    return HttpResponse("You've requested your friends but you don't have any.")

def register(request, template_name):
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

        return render_to_response('registration_page.html', context)


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
    	