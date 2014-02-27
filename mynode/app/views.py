from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from app.models import Comments, Friends, Images, Posts, Users


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

def friends(request):
    return HttpResponse("You've requested your friends but you don't have any.")
