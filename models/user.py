from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)