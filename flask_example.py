import os
import pprint
import sys

from flask import Flask, request, Response

import gitHttpBackend


pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)
git_project_root = sys.argv[1]
print git_project_root


@app.route("/test/<path:path>")
def test(path):
    auth = request.authorization
    if auth:
        username = auth.username
        password = auth.password
        out = {"path": path,
               "authentication": {"username": username, "password": password}}
        out['request'] = request.environ
        return str(('<pre>' + pp.pformat(out) + '</pre>'))
    else:
        return Response(
            'TODO: Why access is denied string goes here...\n',
            401,
            [('WWW-Authenticate', 'Basic realm="Login Required"'),
             ('Content-Type', 'text/plain')]
        )


@app.route('/git/<path:path>', methods=['GET', 'POST'])
def git(path):
    environ = dict(request.environ)
    environ['PATH_INFO'] = environ['PATH_INFO'][4:]
    (
        status_line, headers, response_body_generator
    ) = gitHttpBackend.wsgi_to_git_http_backend(environ, git_project_root)
    return Response(response_body_generator, status_line, headers)


if __name__ == "__main__":
    app.run(debug=True)
