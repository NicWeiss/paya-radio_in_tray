import os
from yandex_music import Client


class Auth:
    def __init__(self):
        self.is_authentificated = False
        self.token_file_path = f'{os.path.dirname(os.path.realpath(__file__))}/tmp/token'

    def auth_with_token(self):
        client = None
        token = None

        if os.path.isfile(self.token_file_path):
            token_file = open(self.token_file_path, 'r')
            token = token_file.read()

        if token:
            print('---------------------- Auth by token ----------------------')
            client = Client(token=token)
            self.is_authentificated = True
        else:
            print('------------------ REQIRED AUTHENTIFICATION ------------------')

        return client

    def authentificate_from_credentials(self, user, password):
        client = None

        if user and password:
            print('---------------------- Auth by credentials ----------------------')

            try:
                client = Client.from_credentials(user, password)
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
