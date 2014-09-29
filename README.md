leanIX SDK for Python
==================

leanIX API version v1, https://developer.leanix.net

Overview
--------
This SDK contains wrapper code used to call the leanIX REST API from Python.

The SDK also contains a simple examples. The code in [samples/ServicesApiSample.py](samples/ServicesApiSample.py) demonstrates the basic use of the SDK to read Applications from the leanIX Inventory.

Prerequisites
-------------

In order to use the code in this SDK, the REST API needs to be activated in your workspace and you need your personal API Key. When you are logged in to leanIX, please go to your profile (click on the user icon in the top menu). You find a menu entry called "API / 3rd party apps". If the REST API is activated, you can generate an API Key here.

You can find the leanIX REST API documentation here https://developer.leanix.net. The documentation is interactive - if you are logged in to your workspace and the REST API is activated, you can try out every function directly from the documentation.

Usage
-----
The following example illustrates how the Api can be used in your python application [samples/ServicesApiSample.py]:
```python
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
```

You can execute the sample with the command

```shell
python ServicesApiSample.py
```

Update SDK
----------
Go into folder codegen and execute
```shell
mvn package
```

Thank You
---------
This API made use of the swagger-* libraries which help you to describe REST APIs in an elegant way. See here for more details: https://github.com/wordnik/swagger-codegen

Copyright and license
------------------------
Copyright 2014 LeanIX GmbH under [the MIT license](LICENSE).
