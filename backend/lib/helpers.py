import functools


def check_auth(f):
    @functools.wraps(f)
    def wrapper(self, *arg, **kw):
        if not self.auth.is_authentificated:
            return {'error': 'Not authentificated!'}

        return f(self, *arg, **kw)
    return wrapper
