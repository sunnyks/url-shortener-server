# URL Shortener

URL shortening server (without persistent storage as of now) using Python.


Server will accept a URL and a short name, check that the URL returns HTTP 200,
then store it in a dictionary and redirect to full URL when requested with
short name. Server will use Post/Redirect/Get design pattern.


Hosted on Heroku @ <http://make-ur-long-url-shorter.herokuapp.com/>

#### External Dependencies:
* requests
