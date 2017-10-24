# URL Shortener

URL shortening server (with no persistent storage) using Python
Server will accept a URL and a short name, check that the URL returns HTTP 200,
then store it in a dictionary and redirect to full URL when requested with
short name. Server will use Post/Redirect/Get design pattern.

#### Dependencies:
..* http
..* requests
..* urllib
