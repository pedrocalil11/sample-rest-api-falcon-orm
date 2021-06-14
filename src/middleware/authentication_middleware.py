import logging
import falcon
from constants import ENV_VARS
from client_exception import NotFoundException, NotAuthorizedException, ForbiddenException
from utils import Utils

class AuthenticationMiddleware(object):
    def process_request(self, req, resp):
        logger = logging.getLogger(__name__)

        # Healthcheck endpoint
        if req.path == '/sample_api/' or req.path == '/sample_api':
            return
        
        # Verifying if Authorization header exists and returning the proper message
        if req.auth is None:
            resp.media = NotAuthorizedException('Authorization header not found', 
                                        'In order to use this API you shall send an header named "Authorization"').get()
            resp.status = falcon.HTTP_401
            resp.complete = True
            return
        
        if req.auth == ENV_VARS["MASTER_ADMIN_KEY"]:
            logger.info("Authenticated using master admin_key")
            return
        else:
            logger.info('Invalid Key was provided')
            resp.media = ForbiddenException('Invalid Key', 'The Key provided on the Authorization header is not valid').get()
            resp.status = falcon.HTTP_403
            resp.complete = True
            return