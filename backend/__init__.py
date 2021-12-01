import json
from urllib.parse import parse_qsl

from yandex_music import Album, Artist, Cover, Track

from backend.controller import Controller


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        album = type(Album())
        artist = type(Artist(0))
        cover = type(Cover())
        track = type(Track(0))

        if type(obj) in [album, artist, cover, track]:
            return obj.__dict__

        return ''


class Router:
    def __init__(self):
        self.controller = Controller()

    def on_request(self, environ, response):
        query_string = environ['QUERY_STRING']
        params = dict(parse_qsl(query_string))
        print(params)
        data = {}

        if 'action' in list(params.keys()):
            self.controller.actions(params['action'])

        if 'get' in list(params.keys()):
            data = self.controller.getters(params['get'])

        body = json.dumps(data, cls=JsonEncoder).encode()
        response("200 OK", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(body)))
        ])

        return iter([body])
