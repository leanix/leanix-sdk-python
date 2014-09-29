#!/usr/bin/env python
"""Unit tests for Python leanIX SDK

Requires you to set three environment varibales:
    API_KEY      your API key

Run all tests:

    python BaseApiTest.py

"""

import sys
import os
import unittest

sys.path = ['../src'] + sys.path
from leanix import *


class BaseApiTest(unittest.TestCase):

    def setUp(self):
        self.apiUrl = os.environ.get('API_URL')
        self.apiKey = os.environ.get('API_KEY')

        client = swagger.ApiClient(self.apiKey, self.apiUrl)
        self.servicesApi = ServicesApi.ServicesApi(client)

if __name__ == "__main__":

    from ServicesApiTest import ServicesApiTest

    unittest.main()
