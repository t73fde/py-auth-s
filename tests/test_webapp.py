#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit test.

:copyright: (c) 2016,2017,2018,2019 by Detlef Stern
:license: Apache 2.0, see LICENSE
"""

import base64
import unittest

import webtest

from py_auth_s import application, get_auth_data


class AuthDataTestCase(unittest.TestCase):
    """Test function get_auth_data."""

    def assert_auth_error(self, username, password):
        """Helper function."""
        self.assertIsNone(username)
        self.assertIsNone(password)

    def check_raw(self, text):
        """Test a raw text for not being able to be decoded."""
        username, password = get_auth_data(text)
        self.assert_auth_error(username, password)

    @staticmethod
    def encode(text):
        """Encode text and prepend basic authentication scheme."""
        return "Basic " + \
            base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def check_encoded(self, text):
        """Test for bad encodings."""
        username, password = get_auth_data(self.encode(text))
        self.assert_auth_error(username, password)

    def check_valid(self, expected_username, expected_password, text):
        """Test for valid encodings."""
        username, password = get_auth_data(self.encode(text))
        self.assertEqual(expected_username, username)
        self.assertEqual(expected_password, password)

    def test_none(self):
        """Test None argument."""
        self.check_raw(None)

    def test_not_basic(self):
        """Must start with 'Basic '."""
        self.check_raw("abc")

    def test_not_base64(self):
        """Must be a Base-64 string."""
        self.check_raw('Basic !"$%&/()')
        self.check_raw('Basic YWJjCg=')

    def test_no_single_colon(self):
        """Must contain a single colon (':')."""
        self.check_encoded('abc')
        self.check_encoded('a:b:c')
        self.check_encoded('')
        self.check_encoded('::')

    def test_valid(self):
        """Valid values must become valid results."""
        self.check_valid('test', '123', 'test:123')
        self.check_valid('', '', ':')
        self.check_valid('', '123', ':123')
        self.check_valid('test', '', 'test:')

    def test_valid_rfc7617(self):
        """Valid values from RFC7671."""
        self.check_valid('Aladdin', 'open sesame', 'Aladdin:open sesame')
        username, password = get_auth_data('Basic dGVzdDoxMjPCow==')
        self.assertEqual('test', username)
        self.assertEqual('123£', password)


class WebappTest(unittest.TestCase):
    """Test the whole webapp."""

    def setUp(self):
        """Set up the web app."""
        self.app = webtest.TestApp(application)

    def test_no_auth(self):
        """Without any authentication, a 401 must be returned."""
        response = self.app.get('/', status=401)
        self.assertIsNotNone(response)

    def test_wrong_auth(self):
        """Wrong authentication results in an 403."""
        self.app.authorization = ('Basic', ('xadmin', '1'))
        response = self.app.get('/', status=403)
        self.assertIsNotNone(response)

    def test_no_password(self):
        """Missing password results in an 403."""
        self.app.authorization = ('Basic', ('xadmin', ''))
        response = self.app.get('/', status=403)
        self.assertIsNotNone(response)

    def test_auth_ok(self):
        """Authorization is ok"""
        self.app.authorization = ('Basic', ('admin', '1'))
        response = self.app.get('/')
        self.assertEqual(200, response.status_int)
