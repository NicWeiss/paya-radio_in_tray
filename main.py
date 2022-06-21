import threading
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

from backend import App
from backend.lib.config_utils import ConfigUtils
from backend.lib.helpers import get_ip


class Main:
    def __init__(self, config):
        self.config = config

        frontend = threading.Thread(name='YaRadio Frontend', target=self.run_frontend)
        frontend.setDaemon(True)
        frontend.start()

        self.backend = App(config)

    def run_frontend(self):
        is_develop = self.config['frontend'].get('is_develop', False)
        print(f'---------------- {is_develop}')
        if is_develop:
            return

        server_address = (get_ip(), self.config['frontend']['port'])
        print(f'Run frontend on {server_address}')
        directory = 'frontend/dist'
        handler = partial(SimpleHTTPRequestHandler, directory=directory)
        httpd = HTTPServer(server_address, handler)
        httpd.serve_forever()


def run(*args):
    config = ConfigUtils().get_config()
    cls = Main(config)

    if config['frontend']['is_open_browser_at_startup']:
        webbrowser.open(f'http://{get_ip()}', config['frontend']['port'])

    return cls.backend.on_request
