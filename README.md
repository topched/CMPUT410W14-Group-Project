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
 
 http://service/author/posts (posts that are visible to the currently authenticated user) 
 To authenticate pass the users ID as a parameter in the URL for example:     http://cs410.cs.ualberta.ca:41061/authors/posts?id=f7s0923kU8d8dD
 
 http://service/posts (all posts marked as public on the server)
 This will retrieve all posts marked as public on our server.
 
 http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
 To authenticate use the method described above.
 
 http://service/posts/{POST_ID} access to a single post with id = {POST_ID}

