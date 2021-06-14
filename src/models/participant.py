from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from models.base import Base

class Participant(Base):
    __tablename__ = 'participant'

    id                          = Column(Integer, primary_key=True)
    sample_round_id               = Column(Integer, ForeignKey('sample_round.id'))
    player_id                   = Column(Integer, ForeignKey('player.id'))
    subscription_date           = Column(DateTime)
    created_at                  = Column(DateTime(timezone=False), server_default=func.now())

    sample_round                  = relationship("SampleRound", back_populates='participants', lazy="joined")  
    player                      = relationship("Player", lazy='joined')

    def __repr__(self):
        return "<Participant(id = '%s', sample_round_id='%s', player_id='%s')>" % (str(self.id), str(self.sample_round_id), str(self.player_id))