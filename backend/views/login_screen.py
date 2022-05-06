
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from backend.lib.notify import Notify
from backend.lib.helpers import close_app


Window.size = (400, 90)


class Layout(GridLayout):
    def __init__(self):

        super(Layout, self).__init__()
        self.login = None
        self.password = None
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 30

        self.add_widget(Label(text='Login or email', size_hint_y=None, height=30))
        login = TextInput(multiline=False, size_hint_y=None, height=30)
        login.bind(text=self.on_input_login)
        self.add_widget(login)

        self.add_widget(Label(text='Password', size_hint_y=None, height=30))
        password = TextInput(password=True, multiline=False, size_hint_y=None, height=30)
        password.bind(text=self.on_input_password)
        self.add_widget(password)

        close = Button(text='Close', size_hint_y=None, height=30)
        close.bind(state=self.end_func)

        login = Button(text='Login', size_hint_y=None, height=30)
        login.bind(state=self.auth)

        self.add_widget(close)
        self.add_widget(login)

        Window.bind(on_request_close=self.end_func)

    def on_input_login(self, instance, value):
        self.login = value

    def on_input_password(self, instance, value):
        self.password = value

    def end_func(self, *args, **kwargs):
        close_app()

    def auth(self, instance, state):
        from backend.lib.auth import Auth

        if state == 'down':
            if not self.login or not self.password:
                Notify().error('Не указаны учётный данные')
                return

            print(f'Auth {self.login} with {self.password}')
            result = Auth().authentificate_from_credentials(self.login, self.password)

            if not result:
                Notify().error('Авторизация не удалась!')
            else:
                Notify().success('Токен получен')
                Window.close()
                exit(0)


class GuiApp(App):
    def build(self):
        self.icon = f"{os.path.dirname(__file__)}/../assets/icon.png"
        self.title = 'Ya.Radio Desktop by NicWeiss | AUTH'
        return Layout()


class LoginScreen:
    def show(self):
        GuiApp().run()
