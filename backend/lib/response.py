from backend.lib.jsonify import jsonify


def create_resonse(response, code='200 ok', data='{}'):
    body = jsonify(data)
    response(code, [
        ('Access-Control-Allow-Headers', '*'),
        ('Access-Control-Allow-Origin', '*'),
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body)))
    ])

    return iter([body])
