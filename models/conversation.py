from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    identity_id = Column(
        Integer,
        ForeignKey("identities.id"),
        nullable=False
    )

    title = Column(String(255), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )