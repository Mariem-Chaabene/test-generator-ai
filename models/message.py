from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(Enum("user", "assistant"))
    content = Column(Text)