import falcon
import logging
import os
import json
import traceback

# General Utilities
from constants import ENV_VARS

# Middlewares
from falcon_multipart.middleware                import MultipartMiddleware
from middleware.logger                          import Logger
from middleware.session_manager                 import SessionManager
from middleware.authentication_middleware       import AuthenticationMiddleware

# Resources
from resources.health_check                     import HealthcheckResource
from resources.sample_round                       import SampleRoundResource
from resources.participant                      import ParticipantResource
from resources.player                             import PlayerResource

from sqlalchemy                                 import create_engine
from sqlalchemy.orm                             import sessionmaker

logging.basicConfig(format='%(process)d - [%(name)20.20s] [%(levelname)6.6s] %(message)s', level=logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

def create():
    db_hostname = ENV_VARS['DB_HOSTNAME']
    db_port = ENV_VARS['DB_PORT']
    db_username = ENV_VARS['DB_USERNAME']
    db_name = ENV_VARS['DB_NAME']
    db_password = ENV_VARS['DB_PASSWORD']
            
    if ENV_VARS['APP_ENV'] == 'local':
        engine = create_engine(("postgresql://" + db_username + ":" + db_password + "@" + db_hostname + ":" + db_port
                            + "/" + db_name), echo=False, pool_size=5, max_overflow=2, pool_pre_ping=True)
    else:
        engine = create_engine(("postgresql://" + db_username + ":" + db_password + "@" + db_hostname + ":" + db_port
                                + "/" + db_name + "?sslmode=verify-ca&sslrootcert=/rds-ca-2019-root.pem"), pool_size=5, max_overflow=2, pool_pre_ping=True)
        
    session_maker = sessionmaker(bind=engine)

    api = falcon.API(middleware=[ Logger(), 
                                    SessionManager(session_maker),
                                    AuthenticationMiddleware() ])
    # Healthcheck
    health_check_resource = HealthcheckResource()
    api.add_route('/sample_api', health_check_resource)
    api.add_route('/sample_api/{place_holder}', health_check_resource)

    player_resource = PlayerResource()
    api.add_route('/sample_api/player', player_resource),
    api.add_route('/sample_api/player/{player_key}', player_resource, suffix="by_key")

    sample_round_resource = SampleRoundResource()
    api.add_route('/sample_api/sample_round', sample_round_resource),
    api.add_route('/sample_api/sample_rounds', sample_round_resource, suffix="list"),
    api.add_route('/sample_api/sample_round/{sample_round_key}', sample_round_resource, suffix="by_key")

    participant_resource = ParticipantResource()
    api.add_route('/sample_api/sample_round/{sample_round_key}/participant', participant_resource),
    api.add_route('/sample_api/sample_round/{sample_round_key}/participants', participant_resource, suffix="list"),
    api.add_route('/sample_api/sample_round/{sample_round_key}/participant/{player_key}', participant_resource, suffix="by_key")


    return api

api = application = create()


class ErrorHandler:
    @staticmethod
    def http(ex, req, resp, params):
        raise

    @staticmethod
    def unexpected(ex, req, resp, params):
        logging.fatal(traceback.format_exc(limit=10))
        # TODO - Improve stack tracing logging
        raise falcon.HTTPInternalServerError("Internal Server Error",
                                             "There was an internal server error, please try again later.")


api.add_error_handler(Exception, ErrorHandler.unexpected)
api.add_error_handler(falcon.HTTPError, ErrorHandler.http)
api.add_error_handler(falcon.HTTPStatus, ErrorHandler.http)
