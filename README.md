# LeanIX SDK for Python


LeanIX API version v1, https://developer.leanix.net

## Overview
This SDK contains wrapper code used to call the LeanIX REST API from Python.

The SDK also contains a simple example. The code in [samples/ServicesApiSample.py](samples/ServicesApiSample.py) demonstrates the basic use of the SDK to read Applications from the LeanIX Inventory.

## Prerequisites

### API token
In order to use the code in this SDK, you need an API token to access a workspace.
As a workspace administrator, you can generate it yourself in the LeanIX application under Administration.

The API token acts as credentials to access a LeanIX workspace as the user who generated the token.
Hence you should take care to keep it private, for example by using a password safe application.

The LeanIX REST API uses OAuth2 access tokens to protect its resources. The SDK transparently uses the
API token that is set in the ApiClient to obtain such an access token from the token provider.
The host name of the token provider is normally "svc.leanix.net".

### Swagger documentation

You can find the LeanIX REST API documentation here [https://app.leanix.net/demo/api/v1/](https://app.leanix.net/demo/api/v1/). The documentation is interactive - if you are logged in to your workspace and the REST API is activated, you can try out every function directly from the documentation.

## Usage

The following example illustrates how the Api can be used in your python application [samples/ServicesApiSample.py]:

```python
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
```

It prints the names of all applications which match the full-text search of "design". A API class is used to execute functions. For each Fact Sheet in LeanIX there is one API class, e.g. for the Fact Sheet "Application" the API class is called `ServicesApi`.

You can execute the sample with the command

```shell
python ServicesApiSample.py
```

## Update SDK

If you'd prefer to build the SDK yourself, it's as simple as running

```shell
cd codegen
mvn package
```

Thank You
---------
This API made use of the swagger-* libraries which help you to describe REST APIs in an elegant way. See here for more details: https://github.com/wordnik/swagger-codegen

Copyright and license
------------------------
Copyright 2016 LeanIX GmbH under [the MIT license](LICENSE).
