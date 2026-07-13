from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True
    )


    email = Column(
        String,
        unique=True,
        index=True
    )


    password = Column(
        String
    )


    created_at = Column(
        DateTime,
        server_default=func.now()
    )


    identity = relationship(
        "Identity",
        back_populates="user",
        uselist=False
    )