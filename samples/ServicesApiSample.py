#!/usr/bin/env python

import sys

sys.path = ['../src'] + sys.path
from leanix import *

if __name__ == "__main__":
    client = swagger.ApiClient(apiToken='6x4Kt6QXX4WxfvWOjG4cUnq9Vr3AH6DOkNgTfBgw', tokenProviderHost='svc.leanix.net', basePath='https://app.leanix.net/demo/api/v1')
    servicesApi = ServicesApi.ServicesApi(client)

    services = servicesApi.getServices(filter='design');

    for service in services:
        print service.name
