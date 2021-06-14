import logging
import falcon

from constants                              import ENV_VARS
from controllers.sample_round               import SampleRoundController
from client_exception                       import ClientException
from falcon                                 import HTTPBadRequest
from schema_cache                           import SchemaCache
from falcon.media.validators                import jsonschema


class SampleRoundResource(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_get_by_key(self, req, resp, sample_round_key):
        try:
            self.logger.info("Get sample_round {}".format(sample_round_key))
            sample_round_controller = SampleRoundController(req.context.db_session)
            resp.media = sample_round_controller.get_by_key(sample_round_key)
            resp.status = falcon.HTTP_200
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return
    
    @jsonschema.validate(SchemaCache.getSchema("SampleRound_post.json"))
    def on_post(self, req, resp):
        try:
            self.logger.info("Process sample_round creation with source: {}".format(req.media))
            sample_round_controller = SampleRoundController(req.context.db_session)
            resp.media = sample_round_controller.create(req.media)
            resp.status = falcon.HTTP_200
            return
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return

    def on_get_list(self, req, resp):
        self.logger.info('Processing get sample round list request')
        try:
            sample_round_controller = SampleRoundController(req.context.db_session)
            resp.media = (sample_round_controller.search())
            resp.status = falcon.HTTP_200
            return
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return

