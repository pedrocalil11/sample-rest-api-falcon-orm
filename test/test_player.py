import os
import json
import logging
import uuid
import string
import random
from pytest_steps       import test_steps
from utils              import TestUtils
from setup_tools        import SetupTools

@test_steps(
    "create_player",
    "create_player_bad_schema")
def test_create_player():
    endpoint = "/sample_api/player"

    payload = {
        'name': 'test_player'
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body['player_key'] is not None
    yield

    player_key = str(uuid.uuid4())
    payload = {}
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400
    
    payload = {
        'name': 'test_player',
        'player_key': player_key
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 400
    yield


@test_steps(
    "get_player", 
    "get_player_non_existent")
def test_get_player():
    endpoint = "/sample_api/player"


    payload = {
        'name': 'test_player'
    }
    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    response_body = response.json()
    player_key = response_body['player_key']
    assert player_key is not None

    endpoint = "/sample_api/player/{}".format(player_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body == {}
    yield

    player_key = str(uuid.uuid4())
    endpoint = "/sample_api/player/{}".format(player_key)
    response = TestUtils.make_request('GET', endpoint, api_key="admin")
    assert response.status_code == 404
    yield