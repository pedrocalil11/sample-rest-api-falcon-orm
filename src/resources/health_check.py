from constants import ENV_VARS
import logging
import falcon

class HealthcheckResource(object):
    def on_get(self, req, resp, place_holder = ""):
        logger = logging.getLogger(__name__)
        logger.info('Processing healthcheck request')

        resp.media = {
            'hash': ENV_VARS['GIT_COMMIT'],
            'branch': ENV_VARS['GIT_BRANCH'],
            'environment': ENV_VARS['APP_ENV'],
        }
        resp.status = falcon.HTTP_200