from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.functions import func
from models.base import Base

class Player(Base):
    __tablename__ = 'player'

    id                          = Column(Integer, primary_key=True)
    player_key                    = Column(String)
    name                        = Column(String)
    created_at                  = Column(DateTime(timezone=False), server_default=func.now())

    def __repr__(self):
        return "<Player(id = '%s', name='%s', document_number='%s')>" % (str(self.id), self.name, self.document_number)