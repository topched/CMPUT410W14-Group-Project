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