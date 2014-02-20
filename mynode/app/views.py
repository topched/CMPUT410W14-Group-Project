from django.http import HttpResponse
from django.shortcuts import render
from app.models import Comments, Friends, Images, Posts, Users


def feed(request):
    latest_posts = Posts.objects.all().order_by('date')[:10]
    context = {'latest_posts_list': latest_posts_list}
    return render (request, './feed.html', context)

# Proper response once models are working.
# def friends(request):
#       friends = Friends.objects.all()
#       context = {'friends': friends}
#       return render(request, './friends.html', context)

def friends(request):
    return HttpResponse("You've requested your friends but you don't have any.")
