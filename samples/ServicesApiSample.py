#!/usr/bin/env python

import sys

sys.path = ['../src'] + sys.path
from leanix import *

if __name__ == "__main__":
		client = swagger.ApiClient('<API-KEY>', 'https://app.leanix.net/<WORKSPACE>/api/v1')
		servicesApi = ServicesApi.ServicesApi(client)
		
		services = servicesApi.getServices();
		
		for service in services:
			print service.name
