"""Utility functions to invoke git-http-backend
"""

import logging
import subprocess


# def flask_to_git_http_backend(git_repo_path, environ, start_response):
#     # Parse environ
#     # Ivoke run_git_http_backend
#     # Catch header
#     # start_response
#     # return payload-iterator
#     pass  # TODO


def wsgi_to_git_http_backend(git_repo_path, environ, start_response):
    # Parse environ
    # Ivoke run_git_http_backend
    # Catch header
    # start_response
    # return payload-iterator
    pass  # TODO


def run_git_http_backend(cgi_environ, input_generator, log_std_err=False):
    """Return (header, output_generator)"""
    if log_std_err:
        stderr = subprocess.PIPE
    else:
        stderr = None
    proc = subprocess.Popen(
        ['git', 'http-backend'],
        bufsize=-1,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=stderr,
        env=cgi_environ
    )
    return split_response_generator(proc, input_generator, log_std_err)


def build_cgi_environ(wsgi_environ, git_project_root, user=None):
    """
    Build a CGI environ from a WSGI environment...

    CONTENT_TYPE
    GIT_PROJECT_ROOT = directory containing bare repos
    PATH_INFO (if GIT_PROJECT_ROOT is set, otherwise PATH_TRANSLATED)
    QUERY_STRING
    REMOTE_USER
    REMOTE_ADDR
    REQUEST_METHOD

    If REMOTE_USER is set in wsgi_environ, you should normally leave user
    alone.
    """
    cgi_environ = dict(wsgi_environ)
    for key, value in cgi_environ.iteritems():
        if not isinstance(value, str):
            del cgi_environ[key]
    cgi_environ['GIT_HTTP_EXPORT_ALL'] = '1'
    cgi_environ[GIT_PROJECT_ROOT] = git_project_root
    if user:
        cgi_environ['REMOTE_USER'] = user
    cgi_environ.setdefault('REMOTE_USER', 'unknown')
    return cgi_environ


def _split_response_generator(proc, input_generator, log_std_err):
    """Given a subprocess.Popen object:
    * Start reading stdout (and possibly stderr)
    * Extract the header
    * Construct a generator for everything that comes after the header
    * Return (header, output_generator)
    (The generator is responsible for extracting all data and cleaning up.)"""
    log = logging.getLogger(__name__)
    # TODO: Figure out of a large amount of error data (with no output data)
    # could deadlock us.
    
    pass  # TODO


def _response_generator(proc, input_generator, push_back, log_std_err):
    """docstring for response_generator"""
    pass
