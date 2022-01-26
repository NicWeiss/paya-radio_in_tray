import json
from urllib.parse import parse_qsl

from yandex_music import Album, Artist, Client, Cover, Track

from backend.controller import Controller
from backend.lib.router import Router


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        album = type(Album())
        artist = type(Artist(0))
        client = type(Client())
        cover = type(Cover())
        track = type(Track(0))

        if type(obj) in [album, artist, client, cover, track]:
            return vars(obj)

        if type(obj) == bytes:
            return obj.decode('utf-8')

        return ''


class App:
    def __init__(self):
        self.controller = Controller()
        self.router = Router()
        self.router.collect_pathes(Controller)

    def on_request(self, environ, response):
        if environ['REQUEST_METHOD'] == 'OPTIONS':
            return self.create_resonse(response)

        data = {'action': {}, 'get': {}}
        code = '200 ok'
        path = environ['PATH_INFO']
        query_string = environ['QUERY_STRING']
        query_params = dict(parse_qsl(query_string))
        request_params = {}

        if request_body_size := int(environ.get('CONTENT_LENGTH', 0)):
            request_params = environ['wsgi.input'].read(request_body_size)

        print(f'[{environ["REQUEST_METHOD"]}] {path} {query_params} {request_params}')

        method = self.router.get_method(path)
        # TODO: ниже добавить передачу request_params, если понадобится
        data = getattr(self.controller, method)(query_params) or {}

        if 'error' in data:
            code = '401 Unauthorized'

        return self.create_resonse(response, code, data)

    def create_resonse(self, response, code='200 ok', data={'response': 'ok'}):

        body = json.dumps(data, cls=JsonEncoder).encode()
        response(code, [
            ('Access-Control-Allow-Headers', '*'),
            ('Access-Control-Allow-Origin', '*'),
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(body)))
        ])

        return iter([body])
