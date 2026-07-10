from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from database import Base


class Identity(Base):
    __tablename__ = "identities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    type = Column(
        String,
        default="user"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )