import uuid
import logging
from dateutil.parser                        import parse
from datetime                               import datetime
from sqlalchemy.orm.exc                     import NoResultFound
from sqlalchemy.exc                         import IntegrityError
from controllers.base                       import BaseController
from client_exception                       import NotFoundException, ConflictException, BadRequestException
from models.participant                     import Participant
from models.sample_round                      import SampleRound
from models.player                          import Player
import mappers

class SampleRoundController(BaseController):
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

    def __get_sample_round_by_key(self,sample_round_key):
        try:
            self.logger.info("Trying to get sample_round with key {}".format(sample_round_key))
            retrieved_sample_round = (self.db_session.query(SampleRound).filter(SampleRound.sample_round_key == sample_round_key).one())
            return retrieved_sample_round
        except NoResultFound:
            self.logger.info('SampleRound not found on database, sample_round_key={}'.format(sample_round_key))
            raise NotFoundException('SampleRound not found', 'SampleRound with and sample_round_key="{}" was not found'.format(sample_round_key))

    def get_by_key(self, sample_round_key):
        sample_round = self.__get_sample_round_by_key(sample_round_key)
        sample_round_dto = mappers.SampleRoundMapper.toDTO(sample_round)
        self.db_session.commit()
        return sample_round_dto

    def create(self,sample_round_source):

        new_sample_round = SampleRound()
        new_sample_round.sample_round_key = str(uuid.uuid4())
        new_sample_round.name = sample_round_source['name']
        new_sample_round.start_date = parse(sample_round_source['start_date'])

        try:
            self.db_session.add(new_sample_round)
            sample_round_dto = mappers.SampleRoundMapper.toDTO(new_sample_round)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise ConflictException('Duplicated name', f"name: {sample_round_source['name']} already existent")
        return sample_round_dto

    def search(self):
        self.logger.info('Searching Rounds')

        query = self.db_session.query(SampleRound)
        
        retrieved_rounds = query.all()

        rounds_dto = {
            "rounds": []
        }

        for _round in retrieved_rounds:
            round_dto = mappers.SampleRoundMapper.toDTO(_round)
            rounds_dto["rounds"].append(round_dto)

        self.db_session.commit()
        return rounds_dto