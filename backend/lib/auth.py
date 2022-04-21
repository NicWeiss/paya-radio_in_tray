import os

import urllib3
from yandex_music import Client
from yandex_music.utils.request import Request


class Auth:
    def __init__(self, config):
        proxy = config["backend"]["proxy"]

        self.proxy_url = ''
        self.is_authentificated = False
        self.token_file_path = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp/token'

        if proxy and proxy['enabled']:
            if proxy["user"] and proxy["password"]:
                self.proxy_url = f'http://{ proxy["user"]}:{proxy["password"]}@{proxy["adress"]}:{proxy["port"]}/'
            else:
                self.proxy_url = f'http://{proxy["adress"]}:{proxy["port"]}/'

            print(f'----------- Use proxy -----------')

    def auth_with_token(self):
        client = None
        token = None
        request = Request(proxy_url=self.proxy_url)

        if os.path.isfile(self.token_file_path):
            token_file = open(self.token_file_path, 'r')
            token = token_file.read()

        if token:
            print('---------------------- Auth by token ----------------------')
            client = Client(token=token, request=request)
            self.is_authentificated = True
        else:
            print('------------------ REQIRED AUTHENTIFICATION ------------------')

        return client

    def authentificate_from_credentials(self, user, password):
        client = None
        request = Request(proxy_url=self.proxy_url)

        if user and password:
            print('---------------------- Auth by credentials ----------------------')

            try:
                client = Client.from_credentials(user, password, request=request)
            except Exception:
                return False

            token_file = open(self.token_file_path, 'w')
            token_file.write(client.token)
            token_file.close()
            self.is_authentificated = True

        return client

    def logout(self):
        self.is_authentificated = False
        os.remove(self.token_file_path)

        return True
