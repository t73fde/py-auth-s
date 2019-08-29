#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authentication proxy for student projects.

The proxy can run in different modes:
- LDAP authentication via official HHN production service
- LDAP authentication via official HHN test service
- Authentication via local datastore
- All user are authenticated, except those name starts with an 'x'

:copyright: (c) 2016,2017,2018,2019 by Detlef Stern
:license: Apache 2.0, see LICENSE
"""

import argparse

from py_auth_s import webapp


def main():
    """Test driver."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-D', '--debug', action="store_true", help="enable debugging mode")
    parser.add_argument(
        '-p', '--port', type=int, default=9876,
        help="port number of web server")
    args = parser.parse_args()

    if args.debug:
        from wsgiref.validate import validator
        app = validator(webapp.application)
    else:
        app = webapp.application
    from wsgiref.simple_server import make_server
    server = make_server(host="0.0.0.0", port=args.port, app=app)
    server.serve_forever()


if __name__ == '__main__':
    main()
