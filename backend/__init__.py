import json
from urllib.parse import parse_qsl

from yandex_music import Album, Artist, Client, Cover, Track

from backend.controller import Controller


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        album = type(Album())
        artist = type(Artist(0))
        client = type(Client())
        cover = type(Cover())
        track = type(Track(0))

        if type(obj) in [album, artist, client, cover, track]:
            return vars(obj)

        return ''


class Router:
    def __init__(self):
        self.controller = Controller()

    def on_request(self, environ, response):
        if environ['REQUEST_METHOD'] == 'OPTIONS':
            return self.create_resonse(response)

        data = {'action': {}, 'get': {}}
        code = '200 ok'
        query_string = environ['QUERY_STRING']
        params = dict(parse_qsl(query_string))
        print(params)

        if 'action' in list(params.keys()):
            data['action'] = self.controller.actions(params) or {}

        if 'get' in list(params.keys()):
            data['get'] = self.controller.getters(params) or {}

        if 'error' in data['action'] or 'error' in data['get']:
            code = '401 Unauthorized'

        return self.create_resonse(response, code, data)

    def create_resonse(self, response, code='200 ok', data={'a': 'a'}):
        body = json.dumps(data, cls=JsonEncoder).encode()
        response(code, [
            ('Access-Control-Allow-Headers', '*'),
            ('Access-Control-Allow-Origin', '*'),
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(body)))
        ])

        return iter([body])
