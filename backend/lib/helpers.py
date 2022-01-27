import functools
import socket


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
