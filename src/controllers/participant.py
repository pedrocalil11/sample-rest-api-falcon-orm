import uuid
import logging
from datetime                               import datetime
from sqlalchemy.orm.exc                     import NoResultFound
from sqlalchemy.exc                         import IntegrityError
from controllers.base                       import BaseController
from client_exception                       import NotFoundException, ConflictException, BadRequestException
from models.participant                     import Participant
from models.sample_round                    import SampleRound
from models.player                          import Player
import mappers

class ParticipantController(BaseController):
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

    def __get_participant_by_key(self,sample_round_key,player_key):
        try:
            self.logger.info("Trying to get sample_round with key {}".format(sample_round_key))
            retrieved_sample_round = (self.db_session
                                            .query(Participant)
                                            .join(SampleRound)
                                            .join(Player)
                                            .filter(Player.player_key == player_key)
                                            .filter(SampleRound.sample_round_key == sample_round_key)
                                            .one())
            return retrieved_sample_round
        except NoResultFound:
            self.logger.info('Participant not found on database, sample_round_key={}, player_key:{}'.format(sample_round_key,player_key))
            raise NotFoundException('Participant not found', 'Participant with player_key="{}" and sample_round_key="{}" was not found'.format(player_key,sample_round_key))

    def __get_sample_round_by_key(self,sample_round_key):
        try:
            self.logger.info("Trying to get sample_round with key {}".format(sample_round_key))
            retrieved_sample_round = (self.db_session.query(SampleRound).filter(SampleRound.sample_round_key == sample_round_key).one())
            return retrieved_sample_round
        except NoResultFound:
            self.logger.info('SampleRound not found on database, sample_round_key={}'.format(sample_round_key))
            raise NotFoundException('SampleRound not found', 'SampleRound with and sample_round_key="{}" was not found'.format(sample_round_key))

    def get_by_key(self, sample_round_key,player_key):
        participant = self.__get_participant_by_key(sample_round_key,player_key)
        participant_dto = mappers.ParticipantMapper.toDTO(participant)
        self.db_session.commit()
        return participant_dto

    def get_list(self, sample_round_key):
        sample_round = self.__get_sample_round_by_key(sample_round_key)

        query = self.db_session.query(Participant).join(SampleRound).filter(SampleRound.sample_round_key == sample_round_key).all()
        participant_list = []
        for participant in query:
            participant_dto = mappers.ParticipantMapper.toDTO(participant)
            participant_list.append(participant_dto)
        self.db_session.commit()
        return {
            "participants":participant_list
        }

    def create(self,sample_round_key, participant_source):
        player = self.__get_player_by_key(participant_source['player_key'])
        sample_round = self.__get_sample_round_by_key(sample_round_key)

        _now = datetime.utcnow()
        if sample_round.end_date is not None:
            raise ConflictException("Ended", f"sample_round :{sample_round_key} ended on {sample_round.end_date}")

        try:
            new_participant = Participant()
            new_participant.sample_round = sample_round
            new_participant.player = player
            new_participant.subscription_date = _now

            participant_dto = mappers.ParticipantMapper.toDTO(new_participant)
            self.db_session.add(new_participant)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise ConflictException('Player already registered', "Player {} is already registered on sample_round {}".format(participant_source['player_key'],sample_round_key))

        return participant_dto