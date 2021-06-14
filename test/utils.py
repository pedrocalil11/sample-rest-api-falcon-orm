import logging
import json
from json import JSONDecodeError
from elasticsearch import Elasticsearch
import requests
import os
import boto3
from random import randint


class TestUtils(object):
    @staticmethod
    def log_request(method, endpoint, headers, payload, files):
        logger = logging.getLogger(__name__)
        
        if payload is None:
            payload = ''
        elif payload == '':
            payload = ''
        else:
            try:
                payload = json.dumps(payload, sort_keys=True, indent=4, separators=(',', ': '))
            except JSONDecodeError:
                payload = str(payload)

        logger.info('\n' + method 
                        + '\nEndpoint: ' + endpoint 
                        + '\nHeaders: ' + json.dumps(headers, sort_keys=True, indent=4, separators=(',', ': '))
                        + '\nPayload: ' + payload
                        + '\nFiles: ' + str(len(files.keys())))

    @staticmethod
    def log_response(response):
        logger = logging.getLogger(__name__)

        if response.text == '':
            payload = 'null'
        elif response.text is None:
            payload = 'null'
        else:
            try:
                payload = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': '))
            except JSONDecodeError:
                payload = response.text

        logger.info('\nStatus Code: ' + str(response.status_code) 
                        + '\nTime: ' + str(response.elapsed)
                        + '\nHeaders: ' + json.dumps(dict(response.headers), sort_keys=True, indent=4, separators=(',', ': '))
                        + '\nPayload: ' + payload)

    @staticmethod
    def make_request(method, endpoint, api_key=None, payload = None, quiet=False, files={}, content_type = None, headers = {}):
        port = 3000
        host_address = os.environ['DOCKER_HOST_ADDRESS']

        url = "http://" + host_address + ":" + str(port) + endpoint

        request_headers = {}
        for header_name in headers:
            request_headers[header_name] = headers[header_name]

        if api_key == "admin":
            request_headers["Authorization"] = 'dda5f69d-d456-47e8-b75e-8cbd825d283e'
        elif api_key is not None:
            request_headers["Authorization"] = api_key

        if content_type is not None:
            request_headers['Content-Type'] = content_type
        
        if quiet==False:
            TestUtils.log_request(method, endpoint, request_headers, payload, files)
        
        if len(files.keys()) > 0:
            response = requests.request(method, url, headers=request_headers, files=files)
        elif payload is None and method == 'GET':
            response = requests.request(method, url, headers=request_headers)
        elif payload is None:
            response = requests.request(method, url, headers=request_headers, json={})
        else:
            response = requests.request(method, url, headers=request_headers, json=payload)
        
        if quiet==False:
            TestUtils.log_response(response)
        return response

class Mock(object):
    @staticmethod
    def clear():
        port = 1080
        host_address = os.environ['DOCKER_HOST_ADDRESS']
        uri = 'http://' + host_address + ':' + str(port) + '/mockserver/reset'

        logging.getLogger(__name__).info('Resetting mock')
        
        response = requests.request('PUT', uri)
        if response.status_code != 200:
            raise Exception('Impossible to clear mockserver')
        return response
    
    @staticmethod
    def retrieve_requests(method = None, path=None):
        port = 1080
        host_address = os.environ['DOCKER_HOST_ADDRESS']
        
        uri = 'http://' + host_address + ':' + str(port) + '/mockserver/retrieve?type=requests&format=JSON'
        payload = {}
        
        if method is not None:
            payload['method'] = method
        
        if path is not None:
            payload['path'] = path

        response = requests.request('PUT', uri, json=payload)
        if response.status_code != 200:
            raise Exception('Could not retrieve requests from mockserver, status code: ' + str(response.status_code))
        
        logging.getLogger(__name__).info('Mock requests : {} \nBody: {}'.format(response.status_code, response.json()))

        return response.json()
    
    @staticmethod
    def register_expectations(expectations):
        port = 1080
        host_address = os.environ['DOCKER_HOST_ADDRESS']
        uri = 'http://' + host_address + ':' + str(port) + '/mockserver/expectation'
        requests.request('PUT', uri, json=expectations)
    

    def load_expectations(path):
        with open(path, 'rt') as f:
            expectations = json.load(f)
        
        if isinstance(expectations, list):
            for expectation in expectations:
                Mock.register_expectations(expectation)
        else:
            Mock.register_expectations(expectations)
