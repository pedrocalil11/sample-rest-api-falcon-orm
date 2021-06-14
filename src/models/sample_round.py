from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from models.base import Base

class SampleRound(Base):
    __tablename__ = 'sample_round'

    id                          = Column(Integer, primary_key=True)
    sample_round_key            = Column(String)
    name                        = Column(String)
    start_date                  = Column(DateTime)
    end_date                    = Column(DateTime)
    created_at                  = Column(DateTime(timezone=False), server_default=func.now())

    participants                = relationship("Participant", back_populates="sample_round")

    def __repr__(self):
        return "<SampleRound(id = '%s', name='%s', sample_round_key='%s')>" % (str(self.id), self.name, self.sample_round_key)