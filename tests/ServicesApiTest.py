#!/usr/bin/env python

import sys
import unittest

from BaseApiTest import BaseApiTest

sys.path = ['../src'] + sys.path
from leanix import *


class ServicesApiTest(BaseApiTest):

    def setUp(self):
        super(ServicesApiTest, self).setUp()

    def testGetServices(self):
        res = self.servicesApi.getServices()
        assert res, 'null getServices result'
        assert len(res) != 0, 'number of lists shouldn\'t be 0'


if __name__ == "__main__":
    unittest.main()
