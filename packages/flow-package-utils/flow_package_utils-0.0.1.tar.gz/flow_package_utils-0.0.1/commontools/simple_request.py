# -*- coding: utf-8 -*-
import requests
import json


class EndPoint:

    def __init__(self, endpoint, data=None, headers=None, files=None):
        self.endpoint = endpoint
        self.data = data
        self.headers = {'Authorization': 'Bearer ' + str(headers)}
        self.files = files

    def get_endpoint(self):
        return str(self.endpoint)

    def get(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        r = requests.get(endpoint, params=self.data, headers=self.headers)
        return json.loads(r.text), r.status_code

    def post(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        r = requests.post(endpoint, data=self.data, headers=self.headers,
                          files=self.files)
        return json.loads(r.text), r.status_code

    def post_json(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        self.headers['content-type'] = "application/json"
        data = json.dumps(self.data)
        r = requests.post(endpoint, data=data, headers=self.headers,
                          files=self.files)
        return json.loads(r.text), r.status_code

    def put(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        r = requests.put(endpoint, data=self.data, headers=self.headers,
                         files=self.files)
        return json.loads(r.text), r.status_code

    def put_json(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        self.headers['content-type'] = "application/json"
        data = json.dumps(self.data)
        r = requests.put(endpoint, data=data, headers=self.headers,
                         files=self.files)
        return json.loads(r.text), r.status_code

    def patch(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        r = requests.patch(endpoint, data=self.data, headers=self.headers)
        return json.loads(r.text), r.status_code

    def delete(self):
        endpoint = EndPoint(self.endpoint).get_endpoint()
        r = requests.delete(endpoint, data=self.data, headers=self.headers)
        return json.loads(r.text), r.status_code
