import sys

sys.path = ['../src'] + sys.path

from leanix import *

if __name__ == "__main__":
    client = swagger.ApiClient(apiToken='LVdc8Ns95w45x4SxLxcnxw5EawxdueqYW3b6wHXL', tokenProviderHost='test-svc.leanix.net', basePath='https://test-app.leanix.net/artemdemo/api/v1')
    capabilitiesApi = BusinessCapabilitiesApi.BusinessCapabilitiesApi(client)

    capabilities = capabilitiesApi.getBusinessCapabilities(relations='true')

    for bc in capabilities:
        if bc.factSheetHasChildren is not None:
            for ch in bc.factSheetHasChildren:
                print ch

    for bc in capabilities:
        print 'Children of ' + bc.name + ':\n'
        if bc.factSheetHasChildren is not None:
            # This is a dead path even if the response contains children. The deserialization somehow breaks in line swagger.py:163 after first recursive call (objClass = "BusinessCapability")
            for child in bc.factSheetHasChildren:
                print '> ' + child + '\n'