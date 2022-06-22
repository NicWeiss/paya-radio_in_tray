import functools
import os
import socket
import subprocess


def check_auth(f):
    @functools.wraps(f)
    def wrapper(self, *arg, **kw):
        if not self.auth.is_authentificated:
            return {'error': 'Not authentificated!'}

        return f(self, *arg, **kw)
    return wrapper


def get_ip():
    ip = '127.0.0.1'

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("1.2.3.4", 80))
        ip = sock.getsockname()[0]
    except Exception:
        pass

    return ip


def set_lock(name):
    lock_path = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp/{name}'
    file = open(lock_path, "w+")
    file.write("Locked")
    file.close()


def is_locked(name):
    lock_path = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp/{name}'
    return os.path.isfile(lock_path)


def clear_lock(name):
    lock_path = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp/{name}'

    try:
        os.remove(lock_path)
    except Exception:
        pass


def shell(command):
    return subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8")


def close_app():
    os.system(
        'for pid in $(ps aux | grep gunicorn |grep paya_server | awk \'{print $2}\'); do kill -9 $pid; done'
    )
