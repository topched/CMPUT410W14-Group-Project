from django.utils import unittest
from django.test.client import Client
from app.models import *
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
    		last_name="Person"
    		)
        self.app_user = Users.objects.create(user = self.user, git_url="test.git")

        self.post = Post.objects.create(author = self.user, content="My first post")
        self.post_id = self.post.id


    def test_get_stream(self):

    	#No logged in user - should redirect to login
    	resp = self.client.get('/mynode/stream/', follow=True)
    	self.assertRedirects(resp, '/mynode/')


        #Logged user should return the stream page
    	self.client.login(username='admin', password='password')
    	resp = self.client.get('/mynode/stream/')
    	self.assertEqual(resp.status_code, 200)
    	self.assertTemplateUsed(resp, 'stream_page.html')

    def test_create_post(self):

    	posts = Post.objects.all()
    	self.client.login(username='admin',password='password')

    	resp = self.client.post(
    	    '/mynode/stream/post/create/', 
    	    {'content':'My second post'}
    	)

    	tmp = Post.objects.all()
    	
    	self.assertEqual(len(tmp),2)
    	self.assertEqual(tmp[1].content, "My second post")

    def test_delete_post(self):

    	PostToDelete = Post.objects.create(author=self.user,content="A post to delete")
    	self.client.login(username='admin',password='password')

    	posts = Post.objects.all()
    	start = len(posts)

    	url = '/mynode/stream/post/' + str(PostToDelete.id) + '/delete/'

    	resp = self.client.post(url)
    	tmp = Post.objects.all()
    	
    	self.assertEqual(len(tmp), start-1)
    	
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
