import json
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager
from yandex_music import Client
from yandex_music.utils.request import Request

from .notify import Notify


class Auth:
    def __init__(self, config=None):
        proxy = config and config["backend"]["proxy"]

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
            try:
                client = Client(token=token, request=request)
                self.is_authentificated = True
            except:
                Notify().error('Авторизация по токену не удалась')

        if not self.is_authentificated:
            if token := self.get_token():
                self.store_token(token)
                return self.auth_with_token()
            else:
                raise ValueError('Token expected!')

        return client

    def get_token(self):
        def is_active(driver):
            try:
                driver.execute(Command.GET_ALL_COOKIES)
                return True
            except Exception:
                return False

        capabilities = DesiredCapabilities.CHROME
        capabilities["loggingPrefs"] = {"performance": "ALL"}
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        driver = webdriver.Chrome(desired_capabilities=capabilities,
                                  executable_path=ChromeDriverManager().install())
        driver.get(
            "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d")

        token = None

        while token == None and is_active(driver):
            sleep(1)
            logs_raw = []
            try:
                logs_raw = driver.get_log("performance")
            except:
                return

            for lr in logs_raw:
                log = json.loads(lr["message"])["message"]
                url_fragment = log.get('params', {}).get('frame', {}).get('urlFragment')

                if url_fragment:
                    token = url_fragment.split('&')[0].split('=')[1]

        try:
            driver.close()
        except:
            pass

        return token

    def store_token(self, token):
        token_file = open(self.token_file_path, 'w')
        token_file.write(token)
        token_file.close()

    def logout(self):
        self.is_authentificated = False
        os.remove(self.token_file_path)

        return True
