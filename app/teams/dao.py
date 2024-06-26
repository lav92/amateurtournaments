from fastapi import HTTPException, status

from sqlalchemy import select, or_, and_

from app.database import async_session_maker

from app.dao.base import BaseDAO
from app.teams.models import Team
from app.users.models import Users


class TeamDAO(BaseDAO):
    model = Team

    @classmethod
    async def create_team(cls, title: str, abbreviation: str, description: str, capitan: int):
        exiting_team = await TeamDAO.find_or_none(title=title)

        if exiting_team:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Команда с таким названием уже существует"
            )

        await TeamDAO.create(
            title=title,
            abbreviation=abbreviation,
            description=description,
            capitan=capitan.id
        )

    @classmethod
    async def get_my_team(cls, user: Users):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    cls.model.capitan == user.id,
                    cls.model.carry == user.id,
                    cls.model.mid == user.id,
                    cls.model.offlane == user.id,
                    cls.model.support == user.id,
                    cls.model.hard_support == user.id
                )
            )

            team = await session.execute(query)
            return team.scalar_one_or_none()

    @classmethod
    async def get_filled_teams(cls, my_team_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                and_(
                    cls.model.capitan > 0,
                    cls.model.carry > 0,
                    cls.model.mid > 0,
                    cls.model.offlane > 0,
                    cls.model.support > 0,
                    cls.model.hard_support > 0,
                    cls.model.id != my_team_id,
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
