from django.utils import unittest
from django.test.client import Client
from django.test.client import RequestFactory
from django.test import TestCase
from app.models import *
from app.views import *
from django.contrib.auth.models import User

#class MyFuncTestCase(unittest.TestCase):
#    def testBasic(self):
#        a = ['larry', 'curly', 'moe']
#        self.assertEqual(my_func(a, 0), 'larry')
#        self.assertEqual(my_func(a, 1), 'curly')

class GetTests(unittest.TestCase):
    c = Client()
    def testLoginOK(self):
        response = self.c.get('/mynode/')
        self.assertEqual(response.status_code, 200)
    def testRegistrationOK(self):
        response = self.c.get('/mynode/register/')
        self.assertEqual(response.status_code, 200)
    def testAuthOK(self):
        self.username = 'test'
        self.email = 'test@test.com'
        self.password = 'test'
        user = User.objects.create_user(self.username, self.email, self.password)
        Users.objects.create(user = user)
        login = self.c.login(username=self.username, password=self.password)
        self.assertEqual(login, True)

        response = self.c.get('/mynode/profile/')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/mynode/stream/')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/mynode/friends/')
        self.assertEqual(response.status_code, 200)

#Looks like we had a few of the same tests Christian
class testRunner(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="admin",
            email="test@test.com",
            password="password",
            first_name="Admin",
            last_name="Person")

        self.app_user = Users.objects.create(user = self.user, git_url="test.git")

        self.post = Post.objects.create(author = self.user, content="My first post")
        self.post_id = self.post.id

    def test_create_and_confirm_friendship(self):

        tempUser = User.objects.create_user(
            username="testPerson",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")

        temp_appUser = Users.objects.create(user = tempUser, git_url="test.git")

        friends = Friend.objects.all()
        start = len(friends)

        url = '/mynode/friends/friend/create/'

        self.client.login(username='admin',password='password')

        resp = self.client.post(
            url,
            {'receiver_display_name': tempUser.username})

        friends = Friend.objects.all()
        end = len(friends)

        #Friendship created
        self.assertEqual(start, end-1)
        #Admin sends friend request
        self.assertEqual(friends[0].requester,self.user)
        #TempUser receives request
        self.assertEqual(friends[0].receiver,tempUser)
        #friendship should not be accepted yet
        self.assertEqual(friends[0].accepted,0)

        #TODO:Need to POST to this url to confirm friendship -- couldnt get it to work at home
        url1 = '/mynode/friends/' + str(tempUser.id) + '/confirm/'

    def test_create_user(self):

        resp = self.client.get('/mynode/register', follow=True)
        self.assertEqual(resp.status_code, 200)

        tmp = User.objects.all()
        start = len(tmp)

        resp = self.client.post(
            '/mynode/register/',
            {'username':'someUser',
            'email':'fake@fake.com',
            'pwd':'password',
            'surname':'some',
            'lastname':'user',
            'git':'fake.git'})

        tmp = User.objects.all()
        end = len(tmp)

        #Created exactly one new user
        self.assertEqual(end, start+1)
        #Check to make sure the user was created correctly
        self.assertEqual(tmp[end-1].username,'someUser')


    def test_create_post(self):

        posts = Post.objects.all()
        self.client.login(username='admin',password='password')

        resp = self.client.post(
            '/mynode/stream/post/create/', 
            {'content':'My second post'}
        )

        tmp = Post.objects.all()
    
        #Exactly 2 posts after creating a new one
        self.assertEqual(len(tmp),2)
        #Make sure the post contains the correct info
        self.assertEqual(tmp[1].content, "My second post")

    def test_delete_post(self):

        PostToDelete = Post.objects.create(author=self.user,content="A post to delete")
        self.client.login(username='admin',password='password')

        posts = Post.objects.all()
        start = len(posts)

        url = '/mynode/stream/post/' + str(PostToDelete.id) + '/delete/'

        resp = self.client.post(url)
        tmp = Post.objects.all()
    	
    	#Make sure exactly one post was deleted
        self.assertEqual(len(tmp), start-1)

    def test_create_comment(self):

        self.client.login(username='admin',password='password')

        tmp = Comment.objects.all()
        start = len(tmp)

        url = '/mynode/stream/post/' + str(self.post_id) + '/comments/'

        resp = self.client.post(
            url,
            {'parent_post':self.post_id, 'author':self.user, 'content':'My first comment'})

        tmp = Comment.objects.all()
        end = len(tmp)
        
        #Make sure exactly one comment was added
        self.assertEqual(start+1,end)

        val = tmp[end-1].content
        
        #Make sure the comment contains the correct info
        self.assertEqual(val, 'My first comment')

    def test_get_stream(self):

        #No logged in user - should redirect to login
        resp = self.client.get('/mynode/stream/', follow=True)
        self.assertRedirects(resp, '/mynode/')

        #Logged user should return the stream page
        self.client.login(username='admin', password='password')
        resp = self.client.get('/mynode/stream/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stream_page.html')

    def test_get_profile(self):

        #No logged in user - should redirect
        resp = self.client.get('/mynode/profile/', follow=True)
        self.assertRedirects(resp, '/mynode/')

        #Logged in user should return profile page
        self.client.login(username='admin', password='password')
        resp = self.client.get('/mynode/profile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile_page.html')
    	
    def test_get_friends(self):

        #No logged in user - should redirect
        resp = self.client.get('/mynode/friends/', follow=True)
        self.assertRedirects(resp, '/mynode/')

        #Logged in user should return friends page
        self.client.login(username='admin', password='password')
        resp = self.client.get('/mynode/friends/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'friend_page.html')

    def test_get_admin(self):

        #Logged in user
        self.client.login(username='admin', password='password')
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_root_redirect(self):

    	#General root redirection
        resp = self.client.get('/')
        self.assertRedirects(resp, '/mynode/')
