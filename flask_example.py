import pprint

from flask import Flask, request, Response

pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)


@app.route("/<path:path>")
def test(path):
    auth = request.authorization
    username = None
    password = None
    if auth:
        username = auth.username
        password = auth.password
    out = {"path": path,
           "authentication": {"username": username, "password": password}}
    out['request'] = request.environ
    return str(('<pre>' + pp.pformat(out) + '</pre>'))


if __name__ == "__main__":
    app.run(debug=True)
