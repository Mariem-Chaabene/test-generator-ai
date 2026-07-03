<<<<<<< HEAD
from sqlalchemy import Column, Integer, Enum, TIMESTAMP
=======
from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP
>>>>>>> cf32ac958a1882f8fe246d0cb3a200946693257e
from database import Base
import datetime

class Identity(Base):
    __tablename__ = "identities"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True)
=======
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
>>>>>>> cf32ac958a1882f8fe246d0cb3a200946693257e
    type = Column(Enum("guest", "user"), default="guest")
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)