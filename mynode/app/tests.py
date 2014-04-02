__author__ = 'Kris & Christian'
from django.utils import unittest
from django.test.client import Client
from django.test.client import RequestFactory
from django.test import TestCase
from app.models import *
from app.views import *
from django.contrib.auth.models import User
import json

#class MyFuncTestCase(unittest.TestCase):
#    def testBasic(self):
#        a = ['larry', 'curly', 'moe']
#        self.assertEqual(my_func(a, 0), 'larry')
#        self.assertEqual(my_func(a, 1), 'curly')

class GetTests(unittest.TestCase):
    c = Client()
    # def testLoginOK(self):
    #     response = self.c.get('/mynode/')
    #     self.assertEqual(response.status_code, 200)
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

        self.app_user = Users.objects.create(user=self.user, git_url="topched")

        self.post = Post.objects.create(author=self.user, content="My first post")
        self.post_id = self.post.id

    def test_github_feed(self):

        url = "http://api.github.com/users/topched"
        resp = self.client.get(url)

        print resp

    def test_match_friends_from_list(self):

        tempUser1 = User.objects.create_user(
            username="testPerson1",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")

        temp_appUser1 = Users.objects.create(user=tempUser1, git_url="test.git")

        tempUser2 = User.objects.create_user(
            username="testPerson2",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")

        temp_appUser2 = Users.objects.create(user=tempUser2, git_url="test.git")

        tempUser3 = User.objects.create_user(
            username="testPerson3",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")

        temp_appUser3 = Users.objects.create(user=tempUser3, git_url="test.git")

        tempUser4 = User.objects.create_user(
            username="testPerson4",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")

        temp_appUser4 = Users.objects.create(user=tempUser4, git_url="test.git")

        url = '/mynode/friends/friend/create/'

        #admin sends friend request to tempuser1
        self.client.login(username='admin', password='password')
        self.client.post(url,{'receiver_display_name': tempUser1.username})
        self.assertEquals(len(Friend.objects.all()), 1)

        #tempuser1 accepts the friend request
        self.client.login(username=tempUser1.username, password='password')
        url1 = '/mynode/friends/' + str(self.user.id) + '/confirm/'
        self.client.post(url1)
        self.assertEquals(len(Friend.objects.all()), 2)

        #admin sends friend request to tempuser2
        self.client.login(username='admin', password='password')
        self.client.post(url, {'receiver_display_name': tempUser2.username})
        self.assertEquals(len(Friend.objects.all()), 3)

        #tempuser2 accepts friend request
        self.client.login(username=tempUser2.username, password='password')
        url2 = '/mynode/friends/' + str(self.user.id) + '/confirm/'
        self.client.post(url2)
        self.assertEquals(len(Friend.objects.all()), 4)

        #json request to send
        send_json = {}
        send_json['query'] = "friends"
        send_json['author'] = self.app_user.uuid
        send_json['authors'] = [temp_appUser1.uuid, temp_appUser2.uuid, temp_appUser3.uuid, temp_appUser4.uuid]

        #send the post
        url3 = "/service/friends/" + self.app_user.uuid
        resp = self.client.post(url3, data=json.dumps(send_json), content_type="application/json")

        expectedJson = {}
        expectedJson['query'] = 'friends'
        expectedJson['author'] = self.app_user.uuid

        #TODO return proper values in api
        expectedJson['friends'] = [temp_appUser1.uuid, temp_appUser2.uuid]

        #compare response to expected
        return_vals = json.loads(resp.content)
        self.assertEquals(expectedJson, return_vals)

        #send a request with no results
        send_json = {}
        send_json['query'] = 'friends'
        send_json['author'] = temp_appUser4.uuid
        send_json['authors'] = [self.app_user.uuid, temp_appUser1.uuid, temp_appUser2.uuid, temp_appUser3.uuid]

        url4 = "/service/friends/" + temp_appUser4.uuid
        resp = self.client.post(url4, json.dumps(send_json), content_type="application/json")

        expectedJson = {}
        expectedJson['query'] = 'friends'
        expectedJson['author'] = temp_appUser4.uuid
        expectedJson['friends'] = []

        return_vals = json.loads(resp.content)
        self.assertEquals(expectedJson, return_vals)


    def test_create_and_confirm_friendship(self):

        tempUser = User.objects.create_user(
            username="testPerson",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")

        temp_appUser = Users.objects.create(user=tempUser, git_url="test.git")

        friends = Friend.objects.all()
        start = len(friends)

        url = '/mynode/friends/friend/create/'
        self.client.login(username='admin', password='password')

        #print tempUser.username

        self.client.post(
            url,
            {'receiver_display_name': tempUser.username})

        friends = Friend.objects.all()
        end = len(friends)

        #follow created
        self.assertEqual(start, end-1)
        #Admin sends friend request
        self.assertEqual(friends[0].requester,self.user)
        #TempUser receives request
        self.assertEqual(friends[0].receiver,tempUser)
        #friendship should not be accepted yet
        self.assertEqual(friends[0].accepted,0)


        url1 = '/mynode/friends/' + str(self.user.id) + '/confirm/'

        #login and accept friend request
        self.client.login(username='testPerson', password='password')
        resp2 = self.client.post(url1)
        friends = Friend.objects.all()
        self.assertEquals(len(friends), 2)
        self.assertEquals(friends[0].accepted, 1)
        self.assertEquals(friends[1].accepted, 1)


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
            {'content': 'My second post', 'title': 'My test title', 'content-type': 1, 'visibility':1}
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
        self.assertRedirects(resp, '/mynode/login/')

        #Logged user should return the stream page
        self.client.login(username='admin', password='password')
        resp = self.client.get('/mynode/stream/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'stream_page.html')

    def test_get_profile(self):

        #No logged in user - should redirect
        resp = self.client.get('/mynode/profile/', follow=True)
        self.assertRedirects(resp, '/mynode/login/')

        #Logged in user should return profile page
        self.client.login(username='admin', password='password')
        resp = self.client.get('/mynode/profile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile_page.html')
    	
    def test_get_friends(self):

        #No logged in user - should redirect
        resp = self.client.get('/mynode/friends/', follow=True)
        self.assertRedirects(resp, '/mynode/login/')

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

    def test_post_to_api(self):
        #Logged in user
        tempUser1 = User.objects.create_user(
            username="testPerson1",
            email="test@test.com",
            password="password",
            first_name="Test",
            last_name="Person")
        tempUser1.save()
        self.client.login(username='testPerson1', password='password')
        post = Post.objects.create(id=100,author=tempUser1)
        post.save()
        resp = self.client.put('/service/posts/' + str(post.id),
            json.dumps({'content': '1', 'title': 'My test title', 'content-type': 1, 'visibility':1}))
        print resp
        self.assertEqual(Post.objects.get(id=post.id).content, '1')

    #not sure why this test doesnt work
    # def test_root_redirect(self):
    #
    # 	#General root redirection
    #     resp = self.client.get('/')
    #     self.assertRedirects(resp, '/mynode/login/')
