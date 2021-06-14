import logging
from sqlalchemy             import create_engine
from sqlalchemy.orm         import sessionmaker
from sqlalchemy.orm.exc     import NoResultFound
from constants              import ENV_VARS

class BaseController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)