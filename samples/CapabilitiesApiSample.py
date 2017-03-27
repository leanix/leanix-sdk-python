#!/usr/bin/env python

import sys
import json

sys.path = ['../src'] + sys.path
from leanix import *

if __name__ == "__main__":
    client = swagger.ApiClient(apiToken='6x4Kt6QXX4WxfvWOjG4cUnq9Vr3AH6DOkNgTfBgw', tokenProviderHost='svc.leanix.net', basePath='https://app.leanix.net/demo/api/v1')
    capabilitiesApi = BusinessCapabilitiesApi.BusinessCapabilitiesApi(client)

    capabilities = capabilitiesApi.getBusinessCapabilities(relations='true')

    for bc in capabilities:
        print 'Children of ' + bc.name + ':'
        for child in bc.factSheetHasChildren:
            print '> ' + json.dumps(vars(child))
