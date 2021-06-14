import logging
import falcon

from constants                              import ENV_VARS
from controllers.participant                import ParticipantController
from client_exception                       import ClientException
from falcon                                 import HTTPBadRequest
from schema_cache                           import SchemaCache
from falcon.media.validators                import jsonschema


class ParticipantResource(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_get_by_key(self, req, resp, sample_round_key, player_key):
        try:
            self.logger.info("Get sample_round {} participant {}".format(sample_round_key,player_key))
            sample_round_participant_controller = ParticipantController(req.context.db_session)
            resp.media = sample_round_participant_controller.get_by_key(sample_round_key,player_key)
            resp.status = falcon.HTTP_200
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return
    
    def on_get_list(self, req, resp,sample_round_key):
        try:
            self.logger.info("Get sample_round list of partipants")
            sample_round_participant_controller = ParticipantController(req.context.db_session)            
            resp.media = sample_round_participant_controller.get_list(sample_round_key)
            resp.status = falcon.HTTP_200
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return

    @jsonschema.validate(SchemaCache.getSchema("Participant_post.json"))
    def on_post(self, req, resp, sample_round_key):
        try:
            self.logger.info("Creating participant on sample_round {} with source: {}".format(sample_round_key,req.media))
            sample_round_participant_controller = ParticipantController(req.context.db_session)
            resp.media = sample_round_participant_controller.create(sample_round_key,req.media)
            resp.status = falcon.HTTP_200
            return
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return