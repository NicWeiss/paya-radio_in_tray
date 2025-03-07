import time
from hashlib import md5

import requests


class LastFM:
    def __init__(self, config):
        self.config = config.get("lastfm", {})
        self.lastfm_url = "https://ws.audioscrobbler.com/2.0/?format=json"
        self.ap_k = "d3a02eb9087ec95b0a34f448cd8c0edd"
        self.ap_s = "b50f953cab42e6164cf2bc7d319d8dd2"
        self.session_key = ""

        self.get_session()

    def sign(self, data):
        data["api_key"] = self.ap_k

        keys = sorted(data.keys())
        param = [k + data[k] for k in keys]
        param = "".join(param) + self.ap_s
        api_sig = md5(param.encode()).hexdigest()

        data["api_sig"] = api_sig

        return data

    def request(self, data):
        return requests.post(self.lastfm_url, data=self.sign(data))

    def get_session(self):
        data = {
            "method": "auth.getMobileSession",
            "password": self.config.get("password"),
            "username": self.config.get("user"),
        }

        response = self.request(data=data)

        if response.status_code == 200:
            response_json = response.json()
            session = response_json.get("session", {})
            self.session_key = session.get("key", "")

            print(f"[LastFM] Auth is success")
        else:
            print(f"[LastFM] Auth is failed {response.text}")

    def _build_data_by_track(self, track, method):
        return {
            "method": method,
            "artist": track['artists'][0]['name'],
            "track": track['title'],
            "timestamp": str(int(time.time())),
            "album": track['albums'][0]['title'],
            "sk": self.session_key,
        }

    def scrobble_track(self, track, is_retry: bool = False):
        response = self.request(data=self._build_data_by_track(track, "track.scrobble"))

        if response.status_code != 200 and not is_retry:
            self.get_session()
            self.scrobble_track(track, is_retry=True)

        if response.status_code != 200 and is_retry:
            print(f"[LastFM] Failed to scrobble track: {response.text}")
            return

        print(f"[LastFM] Track '{track['title']}' is scrobbled")

    def notify_about_playing_track(self, track, is_retry: bool = False):
        response = self.request(data=self._build_data_by_track(track, "track.updateNowPlaying"))

        if response.status_code != 200 and not is_retry:
            self.get_session()
            self.scrobble_track(track, is_retry=True)

        if response.status_code != 200 and is_retry:
            print(f"[LastFM] Failed to set playing track: {response.text}")
            return

        print(f"[LastFM] Track '{track['title']}' is playing")
