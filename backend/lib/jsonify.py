
import json

from yandex_music import Album, Artist, Client, Cover, Track


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


def jsonify(data):
    return json.dumps(data, cls=JsonEncoder).encode()
