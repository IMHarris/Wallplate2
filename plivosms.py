#!/usr/bin/python3

import requests
import json

PLIVO_VERSION = "v1"
class RestAPI(object):
    def __init__(self,url='https://api.plivo.com', version=PLIVO_VERSION):
        self.version = version
        self.url = url.rstrip('/') + '/' + self.version
        self.auth_id = "MAMDC2YTGZODKZMTQ5OT"
        self.auth_token = "MWEzMmJhYzlkZGY3MTgzNGYxZWVkYWY3NWNlZDBi"
        self._api = self.url + '/Account/%s' % self.auth_id
        self.headers = {'User-Agent':'PythonPlivo'}
        
    def _request(self, method, path, data={}):
            path = path.rstrip('/') + '/'
            if method == 'POST':
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                r = requests.post(self._api + path, headers=headers,
                                  auth=(self.auth_id, self.auth_token),
                                  data=json.dumps(data))
            elif method == 'GET':
                r = requests.get(self._api + path, headers=self.headers,
                                 auth=(self.auth_id, self.auth_token),
                                 params=data)
            elif method == 'DELETE':
                r = requests.delete(self._api + path, headers=self.headers,
                                    auth=(self.auth_id, self.auth_token),
                                    params=data)
            elif method == 'PUT':
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                r = requests.put(self._api + path, headers=headers,
                                 auth=(self.auth_id, self.auth_token),
                                 data=json.dumps(data))
            content = r.content
            if content:
                try:
                    response = json.loads(content.decode("utf-8"))
                except ValueError:
                    response = content
            else:
                response = content
            
            return content
                
    def send_message(self, params=None):
        if not params: params = {}
        return self._request('POST', '/Message/', data=params)
                

