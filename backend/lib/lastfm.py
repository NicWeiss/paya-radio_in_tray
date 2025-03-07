import time
from hashlib import md5

import requests


class LastFM:
    def __init__(self, config):
        self.config = config.get("lastfm", {})
        self.api_key = "d3a02eb9087ec95b0a34f448cd8c0edd"
        self.api_secret = "b50f953cab42e6164cf2bc7d319d8dd2"
        self.session_key = ""

        self.get_session()

    def sign(self, data):
        keys = sorted(data.keys())
        param = [k + data[k] for k in keys]
        param = "".join(param) + self.api_secret
        api_sig = md5(param.encode()).hexdigest()

        data["api_sig"] = api_sig

        return data

    def get_session(self):
        data = {
            "api_key": self.api_key,
            "method": "auth.getMobileSession",
            "password": self.config.get("password"),
            "username": self.config.get("user"),
        }

        response = requests.post("https://ws.audioscrobbler.com/2.0/?format=json", data=self.sign(data))

        if response.status_code == 200:
            response_json = response.json()
            session = response_json.get("session", {})
            self.session_key = session.get("key", "")

            print(f"[LastFM] Auth is success")
        else:
            print(f"[LastFM] Auth is failed {response.text}")

    def scrobble_track(self, track, is_retry: bool = False):
        if track["type"] is None:
            return

        data = {
            "api_key": self.api_key,
            "method": "track.scrobble",
            "artist": track['artists'][0]['name'],
            "track": track['title'],
            "timestamp": str(int(time.time())),
            "album": track['albums'][0]['title'],
            "sk": self.session_key,
        }

        response = requests.post("https://ws.audioscrobbler.com/2.0/?format=json", data=self.sign(data))

        if response.status_code != 200 and not is_retry:
            self.get_session()
            self.scrobble_track(track, is_retry=True)

        if response.status_code != 200 and is_retry:
            print(f"[LastFM] Faled to scrobble track: {response.text}")
            return

        print(f"[LastFM] Track {track['title']} is scrobbled")

