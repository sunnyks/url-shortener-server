# a URL shortener server

import http.server
import requests
from urllib.parse import unquote, parse_qs

memory = {}

# The form where user will enter and submit long URL and shortname
form = '''<!DOCTYPE html>
<title>URL shortener</title>
<form method="POST">
    <label>Long URL:
        <input name="longurl">
    </label>
    <br>
    <label>Short name:
        <input name="shortname">
    </label>
    <br>
    <button type="submit">shorten</button>
</form>
<p>URLs:
<pre>
{}
</pre>
'''

def CheckURL(url, timeout=5):
    # Check whether this url is reachable
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False

class Shortener(http.server.BaseHTTPRequestHandler):
    # Class to handle HTTP requests
    def do_GET(self):
        # GET request will either be for root path ('/') or '/some-name'
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                # Name recognized, redirect to it
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()
            else:
                # Name unrecognized, 404 error
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("Did not recognize '{}'".format(name).encode())
        else:
            # Root path, send HTML form
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            known = "\n".join("{} : {}".format(key, memory[key])
                                for key in sorted(memory.keys()))
            self.wfile.write(form.format(known).encode())

    def do_POST(self):
        # Decode form data
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        # Check that form was completed
        if "longurl" not in params or "shortname" not in params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Fill out the form".encode())
            return

        longurl = params["longurl"][0]
        shortname = params["shortname"][0]

        if CheckURL(longurl):
            # URL is good, remember it
            memory[shortname] = longurl

            # Serve a redirect to HTML form
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            # Failed to fetch URL
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Couldn't fetch '{}'".format(longurl).encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    http_lol = http.server.HTTPServer(server_address, Shortener)
    # Get served.
    http_lol.serve_forever()
