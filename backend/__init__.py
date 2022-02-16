from urllib.parse import parse_qsl

from backend.controller import Controller
from backend.lib.helpers import get_ip
from backend.lib.response import create_resonse
from backend.lib.router import Router


class App:
    def __init__(self, config):
        self.ip = get_ip()
        self.config = config
        self.controller = Controller()
        self.router = Router()
        self.router.collect_pathes(Controller)

    def on_request(self, environ, response):
        if created_response := self.validate_request(environ, response):
            return created_response

        code = '200 ok'
        path = environ['PATH_INFO']
        query_params = dict(parse_qsl(environ['QUERY_STRING']))
        request_params = {}

        if request_body_size := int(environ.get('CONTENT_LENGTH', 0)):
            request_params = environ['wsgi.input'].read(request_body_size)

        print(f'[{environ["REQUEST_METHOD"]}] {path} {query_params} {request_params}')

        method = self.router.get_method(path)
        data = getattr(self.controller, method)(query_params=query_params) or {}

        if 'error' in data:
            code = '401 Unauthorized'

        return create_resonse(response, code, data)

    def validate_request(self, environ, response):
        if not self.config['backend']['is_accept_outside_query']:
            if self.ip != environ['REMOTE_ADDR']:
                return create_resonse(response, '403 Forbidden', {'response': 'Forbidden'})

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            return create_resonse(response)
