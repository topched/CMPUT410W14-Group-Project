CMPUT410W14-Group-Project
=========================

**Required Modules:**<br>
    PIL<br>
    markdown2<br>
    Requests<br>
    SQLite, but local can work on MySql<br>
  
**VM Instructions:**

  To run the server, once you ssh into the VM, navigate to the mynode folder with and run: "python manage.py runserver 0.0.0.0:8080"
  
  To run the server in the background run:"python manage.py runserver 0.0.0.0:8080 &"
  Then to view in the browser run:"./ngrok 8080" 
  
  It will then give you a forwarding url something like this (ex. http://647473cf4.ngrok.com). You can paste this into the browser to access the project. NOTE: The ngrok url will change everytime
  
  To hit the admin page: http://{ ngrok addy }/admin
  
  To hit the main page: http://{ ngrok addy }/mynode
  
**API**

 Our API will respond according to the specifications for the following actions:
 
 http://cs410-06/author/posts (posts that are visible to the currently authenticated user) 
 To authenticate pass the users ID as a parameter in the URL for example:     http://cs410.cs.ualberta.ca:41061/authors/posts?id=f7s0923kU8d8dD
 
 http://cs410-06/posts (all posts marked as public on the server)
 This will retrieve all posts marked as public on our server.
 
 http://cs410-06/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
 To authenticate use the method described above.
 
 http://cs410-06/posts/{POST_ID} access to a single post with id = {POST_ID}
 The post ID being the guid of the post.
 
 http://cs410-06/friends/9de17f29c12e8f97bcbbd34cc908f1baba40658e/8d919f29c12e8f97bcbbd34cc908f19ab9496989
 
 Our service will take two ID's of potential friends and determine whether or not they are truly friends
responds with

    {"query":"friends",
     # or NO
     "friends":"YES"
    }
    
http://cs410-06/friends/9de17f29c12e8f97bcbbd34cc908f1baba40658e
Our server will accept post with the below formatted JSON and return if the author has a friend in the list.

    {"query":"friends",
     "author":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
     "authors":[
    		"7deee0684811f22b384ccb5991b2ca7e78abacde",
    		"539b65f2d76d0327dc45bf6354cda535d6f8ed02",
    		"c55670261253c5ce25e22b47a34629dd15e819d4"
      ]
    }


And we will respond with

    {"query":"friends",
     "author":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
     "friends":[
    		"7deee0684811f22b384ccb5991b2ca7e78abacde",
    		"11c3783f15f7ade03430303573098f0d4d20797b",
      ]
    }

http://cs410-06/friendrequest

Our service will let a user on our

    {"query":"friendrequest",
    "author":{
    "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
    "host":"http://127.0.0.1:5454/",
    "displayname":"Greg"
    },
    "friend": 
                "author":{
                     "id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                     "host":"http://cs410-06/",
                     "displayname":"Lara",
                     "url":"http://cs410.cs.ualberta.ca:41061/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e"
                }
    }

We also implemented a global authors query by

http://cs410-06/global/authors

which returns

    [{'displayname' = 'Jerry', 'id' = 'f2efsdfF54520Oidf0aS'}, ....]
    
** Credit **
Navbar is from http://getbootstrap.com/components/#navbar


