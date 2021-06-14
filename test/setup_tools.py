import json
import random
import string
import uuid
from utils import TestUtils

class SetupTools(object):
    def __init__(self, loto_round_name=None, player_name=None, loto_round_status="created", start_date=None, betting_end_date=None):
        if loto_round_name is None:
            self.loto_round_name = self._generate_random_string()
        else:
            self.loto_round_name = loto_round_name

        payload = {'name': self.loto_round_name}
        if loto_round_status == "created":
            payload['start_date'] = "2100-01-01T18:00:00-03:00"
            payload['betting_end_date'] = "2100-01-02T18:00:00-03:00"
        elif loto_round_status == "opened":
            payload['start_date'] = "2000-01-01T18:00:00-03:00"
            payload['betting_end_date'] = "2100-01-02T18:00:00-03:00"
        elif loto_round_status == "started":
            payload['start_date'] = "2000-01-01T18:00:00-03:00"
            payload['betting_end_date'] = "2000-01-02T18:00:00-03:00"

        if start_date is not None:
            payload['start_date'] = start_date
        if betting_end_date is not None:
            payload['betting_end_date'] = betting_end_date

        endpoint = "/loto_bet/loto_round"
        response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
        assert response.status_code == 200
        response_body = response.json()
        self.loto_round_key = response_body['loto_round_key']

        if player_name is None:
            self.player_name = self._generate_random_string()
        else:
            self.player_name = player_name

        self.player_key = str(uuid.uuid4())
        endpoint = "/loto_bet/player"

        rand_numbers = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 11)])
        self.document_number = "{}.{}.{}-{}".format(rand_numbers[0:3], rand_numbers[3:6], rand_numbers[6:9], rand_numbers[9:11])

        payload = {
            'name': self.player_name,
            'player_key': self.player_key,
            'document_number':self.document_number
        }
        response = TestUtils.make_request('POST', endpoint, api_key="admin", payload=payload)
        assert response.status_code == 200

    def _generate_random_string(self, stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))