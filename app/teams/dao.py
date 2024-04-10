from fastapi import HTTPException, status

from app.dao.base import BaseDAO
from app.teams.models import Team


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
            capitan=capitan
        )
