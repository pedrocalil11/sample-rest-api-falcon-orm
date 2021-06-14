import logging
import falcon

from constants                              import ENV_VARS
from controllers.player                     import PlayerController
from client_exception                       import ClientException
from falcon                                 import HTTPBadRequest
from schema_cache                           import SchemaCache
from falcon.media.validators                import jsonschema


class PlayerResource(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_get_by_key(self, req, resp, player_key):
        try:
            self.logger.info("Get player {}".format(player_key))
            player_controller = PlayerController(req.context.db_session)
            resp.media = player_controller.get_by_key(player_key)
            resp.status = falcon.HTTP_200
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return

    @jsonschema.validate(SchemaCache.getSchema("Player_post.json"))
    def on_post(self, req, resp):
        try:
            self.logger.info("Process player creation with source: {}".format(req.media))
            player_controller = PlayerController(req.context.db_session)
            resp.media = player_controller.create(req.media)
            resp.status = falcon.HTTP_200
            return
        except ClientException as ex:
            resp.media = ex.get()
            resp.status = ex.http_status()
            return
