import asyncio
import threading
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


def on_api_request(environ, start_response):
    query_string = environ['QUERY_STRING']
    print(query_string)

    data = b"Hello!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])


def run_frontend():
  server_address = ('', 7777)
  directory = 'frontend'
  handler = partial(SimpleHTTPRequestHandler, directory=directory)
  httpd = HTTPServer(server_address, handler)
  httpd.serve_forever()


def main(arg):
    frontend = threading.Thread(name='YaRadio Frontend', target=run_frontend)
    frontend.setDaemon(True)
    frontend.start()

    webbrowser.open('http://127.0.0.1:7777')

    return on_api_request
