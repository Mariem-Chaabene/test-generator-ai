from sqlalchemy import Column, Integer, Enum, TIMESTAMP
from database import Base
import datetime

class Identity(Base):
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True)
    type = Column(Enum("guest", "user"), default="guest")
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)