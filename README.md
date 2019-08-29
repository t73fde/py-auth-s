# py-auth-s
Simple HTTP Basic Authentication Web Server (Python).

Provides a simple web server that acts as an authentication server, mostly for
development purposes. This is the Python version. There is also a [Go
version](https://github.com/t73fde/go-auth-s). See there for more details.

The easiest way to use this service is to build an docker image and to run it:

    make build
    make run-dev

Or run it directly:

    PYTHONPATH=. python py_auth_s/main.py
