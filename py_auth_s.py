#!/usr/bin/env python

"""
HTTP Basic authentication service for development

:copyright: (c) 2016,2017,2018,2019 by Detlef Stern
:license: Apache 2.0, see LICENSE
"""

import argparse
import base64
import binascii
import os


BASIC_AUTH_TEXT = "basic "
REALM = "Default"


def check_password(username, password):
    """Check authorization of user name and password."""
    return username and password and not username.startswith("x")


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


def main():
    """Test driver."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', type=int, default=9876,
        help="port number of web server")
    args = parser.parse_args()

    from wsgiref.simple_server import make_server
    print("Listening on port", args.port)
    server = make_server(host="0.0.0.0", port=args.port, app=application)
    server.serve_forever()


if __name__ == '__main__':
    main()
