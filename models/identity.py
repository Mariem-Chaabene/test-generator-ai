
from sqlalchemy import Column, Integer, Enum, TIMESTAMP

from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP

from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP
from database import Base
import datetime

class Identity(Base):
    __tablename__ = "identities"


    id = Column(Integer, primary_key=True)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(Enum("guest", "user"), default="guest")
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)