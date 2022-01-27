import threading
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

from backend import App
from backend.lib.helpers import get_ip


class Main:
    def __init__(self, config):
        frontend = threading.Thread(name='YaRadio Frontend', target=self.run_frontend)
        frontend.setDaemon(True)
        frontend.start()

        self.backend = App()

    def run_frontend(self):
        server_address = (get_ip(), 7777)
        print(f'Run frontend on {server_address}')
        directory = 'frontend'
        handler = partial(SimpleHTTPRequestHandler, directory=directory)
        httpd = HTTPServer(server_address, handler)
        httpd.serve_forever()


def run(config):
    cls = Main(config)

    # webbrowser.open('http://127.0.0.1:7777')
    return cls.backend.on_request
