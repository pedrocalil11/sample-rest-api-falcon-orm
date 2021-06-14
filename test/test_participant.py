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
    "create_participant",
    "create_participant_duplicated",
    "create_participant_inexistent_player", 
    "create_participant_inexistent_sample_round",
    "create_participant_bad_schema")
def test_create_participant():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_round"

    round_name = ''.join(random.choice(letters) for i in range(10))
    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    sample_round_key = response_body['sample_round_key']

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
    response_body = response.json()
    assert response_body['sample_round']['sample_round_key'] == sample_round_key
    assert response_body['subscription_date'] is not None
    yield

    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 409
    yield

    endpoint = "/sample_api/sample_round/{}/participant".format(sample_round_key)
    payload = {"player_key": "60271ff2-292b-4e12-a12b-13f6086f3323"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 404
    yield

    endpoint = "/sample_api/sample_round/60271ff2-292b-4e12-a12b-13f6086f3323/participant"
    payload = {"player_key": player_key}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 404
    yield

    payload = {
        "player_key": "dksmdlsmda"
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400
    payload = {
        "player_key": str(uuid.uuid4()),
        "error":"as"
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400    
    payload = {}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400    
    yield

@test_steps(
    "get_participant_non_attributed",
    "get_participant",
    "get_participant_non_existent_player",
     "get_participant_non_existent_round")
def test_get_participant():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_round"

    round_name = ''.join(random.choice(letters) for i in range(10))
    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    sample_round_key = response_body['sample_round_key']

    endpoint = "/sample_api/player"

    payload = {
        'name': 'test_player'
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    player_key = response_body['player_key']

    endpoint = "/sample_api/sample_round/{}/participant/{}".format(sample_round_key, player_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 404
    yield

    endpoint = "/sample_api/sample_round/{}/participant".format(sample_round_key)
    payload = {"player_key": player_key}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    endpoint = "/sample_api/sample_round/{}/participant/{}".format(sample_round_key, player_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['sample_round']['sample_round_key'] == sample_round_key
    assert response_body['subscription_date'] is not None
    yield

    endpoint = "/sample_api/sample_round/{}/participant/60271ff2-292b-4e12-a12b-13f6086f3323".format(sample_round_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 404
    yield

    endpoint = "/sample_api/sample_round/60271ff2-292b-4e12-a12b-13f6086f3323/participant/{}".format(player_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 404
    yield

@test_steps(
    "get_list_empty",
    "get_list",
    "get_list_non_existent")
def test_get_list():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_round"

    round_name = ''.join(random.choice(letters) for i in range(10))
    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    sample_round_key = response_body['sample_round_key']

    endpoint = "/sample_api/sample_round/{}/participants".format(sample_round_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body['participants']) == 0
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

    endpoint = "/sample_api/sample_round/{}/participants".format(sample_round_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body['participants']) == 1
    yield

    endpoint = "/sample_api/sample_round/60271ff2-292b-4e12-a12b-13f6086f3323/participants"
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 404
    yield