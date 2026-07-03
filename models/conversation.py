from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    identity_id = Column(Integer, ForeignKey("identities.id"))
    title = Column(String(255))