from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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
        ForeignKey("users.id"),
        nullable=True
    )


    type = Column(
        String,
        default="guest"
    )


    created_at = Column(
        DateTime,
        server_default=func.now()
    )


    user = relationship(
        "User",
        back_populates="identity"
    )