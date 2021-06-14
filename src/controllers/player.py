import uuid
import logging
import math
from datetime                               import datetime
from sqlalchemy.orm.exc                     import NoResultFound
from sqlalchemy.exc                         import IntegrityError
from controllers.base                       import BaseController
from client_exception                       import NotFoundException, ConflictException, BadRequestException
from models.participant                     import Participant
from models.sample_round                      import SampleRound
from models.player                          import Player
import mappers

class PlayerController(BaseController):
    def __init__(self, db_session):
        BaseController.__init__(self)
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)

    def __get_player_by_key(self,player_key):
        try:
            self.logger.info("Trying to get player with key {}".format(player_key))
            retrieved_player = self.db_session.query(Player).filter(Player.player_key == player_key).one()
            return retrieved_player
        except NoResultFound:
            self.logger.info('Player not found on database, player_key={}'.format(player_key))
            raise NotFoundException('Player not found', 'player with and player_key="{}" was not found'.format(player_key))

    def get_by_key(self, player_key):
        player = self.__get_player_by_key(player_key)
        self.db_session.commit()
        return {}

    def create(self,player_source):
        new_player = Player()

        new_player.player_key = str(uuid.uuid4())
        new_player.name = player_source['name']

        self.logger.info("Adding player from session")
        self.db_session.add(new_player)
        self.db_session.commit()

        return {
            "player_key": new_player.player_key
        }
