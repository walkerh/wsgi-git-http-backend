from flask import Flask, request, Response

from gitHttpBackend import run_git_http_backend

app = Flask(__name__)


# note: there will be other routes - add them as needed
@app.route('/<user>/<repo>.git/info/refs')
def git_request(user, repo):
    cgi_environment = dict(
        (key, value) for key, value in request.environ.iteritems()
        if isinstance(value, basestring))
    cgi_environment['GIT_PROJECT_ROOT'] = '/Users/wilsaj/git-server/repos/'

    # PATH_INFO might be wrong - not sure what the GIT expects here
    cgi_environment['PATH_INFO'] = './some_repo/'

    headers, response_generator = run_git_http_backend(
            cgi_environment,
            request.environ)

    return Response(response_generator, headers=headers)
