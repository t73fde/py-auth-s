"""
Authentication proxy for student projects.

WSGI web application.

:copyright: (c) 2016 by Detlef Stern
:license: Apache 2.0, see LICENSE
"""

import base64
import binascii
import os


BASIC_AUTH_TEXT = "basic "
REALM = "Default"


def get_passwords():
    """Try to read password from a file."""
    file_name = os.environ.get('PWFILE')
    if file_name is None:
        return None
    result = {}
    try:
        with open(file_name, 'r') as auth_file:
            for line in auth_file:
                data = line.strip().split(':')
                if len(data) == 2:
                    result[data[0]] = data[1]
        return result
    except FileNotFoundError:
        return None
    return None


PASSWORD_DICT = get_passwords()


def check_password(username, password):
    """Check authorization of user name and password."""
    if PASSWORD_DICT is not None:
        return PASSWORD_DICT.get(username, 0) == password
    if not username or not password:
        return False
    if username.startswith("x"):
        return False
    return True


def get_auth_data(authorization):
    """Retrieve user name and password from HTTP header 'Authorization:'."""
    if authorization is None:
        return (None, None)
    if not authorization.lower().startswith(BASIC_AUTH_TEXT):
        return (None, None)
    encoded_auth = authorization[len(BASIC_AUTH_TEXT):]
    try:
        decoded_auth = base64.b64decode(encoded_auth).decode('utf-8')
    except binascii.Error:
        return (None, None)
    auth_data = decoded_auth.split(':')
    if len(auth_data) != 2:
        return (None, None)
    return (auth_data[0], auth_data[1])


def application(environ, start_response):
    """WSGI web application."""
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', '0'),
    ]
    username, password = get_auth_data(environ.get('HTTP_AUTHORIZATION'))
    if username is None:
        response_headers.append(
            ('WWW-Authenticate',
             '{}realm="{}"'.format(BASIC_AUTH_TEXT, REALM)))
        start_response('401 Unauthorized', response_headers)
    elif not check_password(username, password):
        start_response('403 Forbidden', response_headers)
    else:
        start_response('200 OK', response_headers)
    return []
