from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    abbreviation = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    capitan = Column(ForeignKey('users.id'))
    carry = Column(ForeignKey('users.id'))
    mid = Column(ForeignKey('users.id'))
    offlane = Column(ForeignKey("users.id"))
    support = Column(ForeignKey("users.id"))
    hard_support = Column(ForeignKey("users.id"))
