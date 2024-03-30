from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.teams.schemas import SchemaCreateTeam
from app.users.models import User
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO
from app.teams.models import Team

router = APIRouter(
    prefix='/team',
    tags=['Команды']
)


@router.post('/create')
async def create_team(team_data: SchemaCreateTeam, capitan: User = Depends(get_user)):
    exiting_team = await TeamDAO.find_or_none(title=team_data.title)

    if exiting_team:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Команда с таким названием уже существует"
        )

    await TeamDAO.create(
        title=team_data.title,
        abbreviation=team_data.abbreviation,
        description=team_data.description,
        capitan=capitan.id
    )

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=f"{team_data.title} успешно создана"
    )
