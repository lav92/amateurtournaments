from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base

from app.stats.models import Stats


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    nickname = Column(String(255), nullable=True)
    steam_id = Column(BigInteger, nullable=True, default=1)
    role = Column(String(255), nullable=True)

    stats = relationship("Stats", back_populates="user")
