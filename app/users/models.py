from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
