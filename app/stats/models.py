from sqlalchemy import Column, Integer, ForeignKey, String, Float, BigInteger
from sqlalchemy.orm import relationship

from app.database import Base


class Stats(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey("users.id"), nullable=True)
    user = relationship("Users", back_populates="stats")

    match_id = Column(BigInteger, nullable=True)

    hero = Column(String, nullable=True)
    role = Column(String, nullable=True)
    result = Column(String, nullable=True)

    kills = Column(Integer, nullable=True)
    deaths = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    gpm = Column(Integer, nullable=True)
    epm = Column(Integer, nullable=True)
    gold_spent = Column(Integer, nullable=True)
    hero_damage = Column(Integer, nullable=True)
    tower_damage = Column(Integer, nullable=True)
    imp = Column(Integer, nullable=True)
    hero_healing = Column(Integer, nullable=True)

    award = Column(String, nullable=True)

    deal_physical_damage = Column(Integer, nullable=True)
    deal_magic_damage = Column(Integer, nullable=True)
    deal_pure_damage = Column(Integer, nullable=True)
    stun_count = Column(Integer, nullable=True)
    stun_duration = Column(Float, nullable=True)
    disable_count = Column(Integer, nullable=True)
    disable_duration = Column(Float, nullable=True)
    slow_count = Column(Integer, nullable=True)
    slow_duration = Column(Float, nullable=True)
    received_physical_damage = Column(Integer, nullable=True)
    received_magic_damage = Column(Integer, nullable=True)
    received_pure_damage = Column(Integer, nullable=True)
    deal_ability_damage = Column(String(1000), nullable=True)
    deal_item_damage = Column(String(1000), nullable=True)
