#!/usr/bin/env python
"""Wordnik.com's Swagger generic API client. This client handles the client-
server communication, and is invariant across implementations. Specifics of
the methods and models for each application are generated from the Swagger
templates."""

import sys
import os
import re
import urllib
import urllib2
import httplib
import json
import datetime
import base64

from models import *


class ApiClient:
    """
    Generic API client for Swagger client library builds
    """

    def __init__(self, apiToken=None, tokenProviderHost=None , basePath=None):
        self.apiToken = apiToken
        self.oauthTokenUri = 'https://{}/services/mtm/v1/oauth2/token'.format(tokenProviderHost)
        self.accessTokenResponse = None
        self.basePath = basePath
        self.cookie = None

    def __fetchToken(self):
        url = self.oauthTokenUri + '?grant_type=client_credentials'

        headers = {
            'Authorization': 'Basic ' + base64.b64encode('apitoken:' + self.apiToken),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'User-Agent': 'SwaggerClient/LeanIXPySDK',
        }

        request = MethodRequest(method='POST', url=url, headers=headers)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        self.accessTokenResponse = AccessTokenResponse(response=data);


    def callAPI(self, resourcePath, method, queryParams, postData,
                headerParams=None):
        if self.accessTokenResponse is None or self.accessTokenResponse.isExpired():
            self.__fetchToken()

        url = self.basePath + resourcePath
        headers = {
            'Authorization': 'Bearer ' + self.accessTokenResponse.token,
            'User-Agent': 'SwaggerClient/LeanIXPySDK',
        }
        if headerParams:
            for param, value in headerParams.iteritems():
                headers[param] = value

        if self.cookie:
            headers['Cookie'] = self.cookie

        data = None

        if queryParams:
            # Need to remove None values, these should not be sent
            sentQueryParams = {}
            for param, value in queryParams.items():
                if value != None:
                    sentQueryParams[param] = value
            url = url + '?' + urllib.urlencode(sentQueryParams)

        if method in ['GET']:
            #Options to add statements later on and for compatibility
            pass
        elif method in ['POST', 'PUT', 'DELETE']:
            if postData:
                data = self.sanitizeForSerialization(postData)
                if 'Content-type' not in headers:
                    headers['Content-type'] = 'application/json'
                    data = json.dumps(data)
                else:
                    data = urllib.urlencode(data)
        else:
            raise Exception('Method ' + method + ' is not recognized.')

        request = MethodRequest(method=method, url=url, headers=headers,
                                data=data)

        # Make the request
        response = urllib2.urlopen(request)
        if 'Set-Cookie' in response.headers:
            self.cookie = response.headers['Set-Cookie']
        string = response.read()

        try:
            data = json.loads(string)
        except ValueError:  # PUT requests don't return anything
            data = None

        return data

    def toPathValue(self, obj):
        """
        Convert a string or object to a path-friendly value
        Args:
            obj -- object or string value
        Returns:
            string -- quoted value
        """
        if type(obj) == list:
            return urllib.quote(','.join(obj))
        else:
            return urllib.quote(str(obj))

    def sanitizeForSerialization(self, obj):
        """
        Dump an object into JSON for POSTing.
        """

        if obj is None:
            return None
        elif type(obj) in [str, int, long, float, bool, unicode]:
            return obj
        elif isinstance(obj, list):
            return [self.sanitizeForSerialization(subObj) for subObj in obj]
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            if isinstance(obj, dict):
                objDict = obj
            else:
                objDict = obj.__dict__
            return {key: self.sanitizeForSerialization(val)
                    for (key, val) in objDict.iteritems()
                    if key != 'swaggerTypes'}

    def deserialize(self, obj, objClass):
        """
        Deserialize a JSON string into an object.

        Args:
            obj -- string or object to be deserialized
            objClass -- class literal for deserialzied object, or string
                of class name
        Returns:
            object -- deserialized object
        """

        # Have to accept objClass as string or actual type. Type could be a
        # native Python type, or one of the model classes.
        if isinstance(objClass, str):
            if 'Array[' in objClass:
                match = re.match('Array\[(.*)\]', objClass)
                subClass = match.group(1)
                return [self.deserialize(subObj, subClass) for subObj in obj]

            if (objClass in ['int', 'float', 'long', 'dict', 'list', 'str', 'bool', 'datetime', 'unicode']):
                objClass = eval(objClass)
            else:  # not a native type, must be model class
                objClass = eval(objClass + '.' + objClass)

        if objClass in [int, long, float, dict, list, str, bool]:
            return objClass(obj)
        elif objClass == datetime:
            # Server will always return a time stamp in UTC, but with
            # trailing +0000 indicating no offset from UTC. So don't process
            # last 5 characters.
            return datetime.datetime.strptime(obj[:-6],
                                              "%Y-%m-%dT%H:%M:%S")

        instance = objClass()

        for attr, attrType in instance.swaggerTypes.iteritems():
            if obj is not None and attr in obj and type(obj) in [list, dict]:
                value = obj[attr]
                if attrType in ['str', 'int', 'long', 'float', 'bool']:
                    attrType = eval(attrType)
                    try:
                        value = attrType(value)
                    except UnicodeEncodeError:
                        value = unicode(value)
                    except TypeError:
                        value = value
                    setattr(instance, attr, value)
                elif (attrType == 'datetime'):
                    setattr(instance, attr, datetime.datetime.strptime(value[:-6],
                                              "%Y-%m-%dT%H:%M:%S"))
                elif 'Array[' in attrType:
                    match = re.match('Array\[(.*)\]', attrType)
                    subClass = match.group(1)
                    subValues = []
                    if not value:
                        setattr(instance, attr, None)
                    else:
                        for subValue in value:
                            subValues.append(self.deserialize(subValue,
                                                              subClass))
                    setattr(instance, attr, subValues)
                else:
                    setattr(instance, attr, self.deserialize(value,
                                                             objClass))

        return instance


class MethodRequest(urllib2.Request):

    def __init__(self, *args, **kwargs):
        """Construct a MethodRequest. Usage is the same as for
        `urllib2.Request` except it also takes an optional `method`
        keyword argument. If supplied, `method` will be used instead of
        the default."""

        if 'method' in kwargs:
            self.method = kwargs.pop('method')
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return getattr(self, 'method', urllib2.Request.get_method(self))


class AccessTokenResponse:
    # Token needs to be at least 60 sec valid, otherwise it is considered expired
    LEAD_TIME = 60;

    def __init__(self, response=None):
        self.token = response['access_token']
        self.expires = datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])

    def isExpired(self):
        return self.expires - datetime.timedelta(seconds=self.LEAD_TIME) < datetime.datetime.now()

