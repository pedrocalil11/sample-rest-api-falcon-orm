import os
import json
import logging
import uuid
import string
import random
import datetime
import time
from pytest_steps       import test_steps
from utils              import TestUtils
from setup_tools        import SetupTools

@test_steps(
    "create_sample_round",
    "create_sample_round_duplicated_name",
    "create_sample_round_bad_schema")
def test_create_sample_round():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_round"

    round_name = ''.join(random.choice(letters) for i in range(10))
    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['name'] == round_name
    assert response_body['sample_round_key'] is not None
    assert response_body['start_date'] is not None
    assert response_body['end_date'] is None
    assert response_body['number_of_participants'] == 0
    yield

    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 409
    yield

    payload = {'name': ''.join(random.choice(letters) for i in range(10)), "test": "teste"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400
    payload = {"start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400
    payload = {}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400
    yield

@test_steps(
    "get_sample_round",
    "get_sample_round_with_player", 
    "get_sample_round_non_existent")
def test_get_sample_round():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_round"

    round_name = ''.join(random.choice(letters) for i in range(10))
    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    sample_round_key = response_body['sample_round_key']

    endpoint = "/sample_api/sample_round/{}".format(sample_round_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['name'] == round_name
    assert response_body['sample_round_key'] is not None
    assert response_body['start_date'] is not None
    assert response_body['end_date'] is None
    assert response_body['number_of_participants'] == 0
    yield

    endpoint = "/sample_api/player"

    payload = {
        'name': 'test_player'
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    player_key = response_body['player_key']

    endpoint = "/sample_api/sample_round/{}/participant".format(sample_round_key)
    payload = {"player_key": player_key}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    endpoint = f"/sample_api/sample_round/{sample_round_key}"
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['sample_round_key'] is not None
    assert response_body['start_date'] is not None
    assert response_body['end_date'] is None
    assert response_body['number_of_participants'] == 1
    yield

    sample_round_key = str(uuid.uuid4())
    endpoint = "/sample_api/sample_round/{}".format(sample_round_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 404
    yield

@test_steps(
    "search_previous_verifications", 
    "search_sample_round_full")
def test_search_sample_round():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_rounds"
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    total = len(response_body['rounds'])
    yield

    endpoint = "/sample_api/sample_round"

    payload = {'name': ''.join(random.choice(letters) for i in range(10)), "start_date": "2030-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200

    endpoint = "/sample_api/sample_rounds"
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body['rounds']) == total + 1
    yield