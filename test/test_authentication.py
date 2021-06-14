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
    "no_authorization",
    "invalid_authorization",
    "success"
)
def test_authorization():
    letters = string.ascii_lowercase

    endpoint = "/sample_api/sample_round"

    round_name = ''.join(random.choice(letters) for i in range(10))
    payload = {'name': round_name, "start_date": "2020-01-01T18:00:00-03:00"}
    response = TestUtils.make_request('POST', endpoint, api_key=None, payload=payload)
    assert response.status_code == 401
    yield

    response = TestUtils.make_request('POST', endpoint, api_key=str(uuid.uuid4()), payload=payload)
    assert response.status_code == 403
    yield

    response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
    assert response.status_code == 200
    yield