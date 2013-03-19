"""Utility functions to invoke git-http-backend
"""

import logging
import subprocess
import threading


CHUNK_SIZE = 0x8000


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


def run_git_http_backend(cgi_environ, input_string_io, log_std_err=False):
    """Return (header, output_generator)"""
    if log_std_err:
        stderr = subprocess.PIPE
    else:
        stderr = None
    proc = subprocess.Popen(
        ['git', 'http-backend'],
        bufsize=CHUNK_SIZE,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=stderr,
        env=cgi_environ
    )
    return split_response_generator(proc, input_string_io, log_std_err)


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


def _split_response_generator(proc, input_string_io, log_std_err):
    """Given a subprocess.Popen object:
    * Start writing request data
    * Start reading stdout (and possibly stderr)
    * Extract the header
    * Construct a generator for everything that comes after the header
    * Return (header, output_generator)
    (The generator is responsible for extracting all data and cleaning up.)"""
    threading.Thread(target=_input_data_pump,
                     args=(proc, input_string_io)).start()
    if not log_std_err:
        threading.Thread(target=_error_data_pump, args=(proc,)).start()
    output_data_pump = _output_data_pump(proc)
    chunks = []
    header_end = None
    while not header_end:
        chunks.append(proc.stdout.read(CHUNK_SIZE))
        # Search the two most recent chunks for the end of the header.
        # header_end -> (chunk, index) or None
        header_end = _find_header_end_in_2_chunks(*chunks[-2:])
        pass  # TODO
    pass  # TODO


def _input_data_pump(proc, input_string_io):
    # Thread for feeding input to git
    current_data = input_string_io.read(CHUNK_SIZE)
    while current_data:
        proc.stdin.write(current_data)
        current_data = input_string_io.read(CHUNK_SIZE)


def _output_data_pump(proc):
    # Corountine for getting stdout from git
    current_data = proc.stdout.read(CHUNK_SIZE)
    while current_data:
        yield current_data
        current_data = proc.stdout.read(CHUNK_SIZE)


def _error_data_pump(proc):
    # Thread for logging stderr from git
    # TODO: Currently using threads due to lack of universal standard for
    # async event loops in parent applications.
    log = logging.getLogger(__name__)
    for error_message in proc.stderr:
        log.error(error_message)


def _find_header_end_in_2_chunks(chunk0, chunk1):
    # Search for the header end (b'\r\n\r\n') in either the end of the
    # first chunk (with the 4-byte boundary and stretching into the second
    # chunk) or within the second chunk starting at 0. Return as
    # (index_of_chunk, index_within_chunk).
    # Return None if header end not found.
    boundary_string = chunk0[-3:] + chunk1[:3]
    hit = _search_str_for_header_end(boundary_string)
    if hit is not None:
        return 0, len(chunk0) - 3 + hit
    hit = _search_str_for_header_end(chunk1)
    if hit is not None:
        return 1, hit


def _response_generator(proc, input_string_io, push_back, log_std_err):
    """docstring for response_generator"""
    pass
