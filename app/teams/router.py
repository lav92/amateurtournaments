from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form

from app.teams.schemas import SchemaCreateTeam
from app.users.models import User
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO
from app.templates.templates import templates

router = APIRouter(
    prefix='',
    tags=['Команды']
)


# Frontend URLs
@router.get("/create-team")
async def create_team(request: Request):
    return templates.TemplateResponse(name='create-team.html', context={"request": request})


@router.post("/building_team")
async def build_team(
        request: Request,
        title: str = Form(),
        abbreviation: str = Form(),
        description: str = Form(),
        capitan: User = Depends(get_user),
):
    team = await TeamDAO.create_team(
        title=title,
        abbreviation=abbreviation,
        description=description,
        capitan=capitan.id,
    )

    return templates.TemplateResponse(name='home.html', context={"request": request, "team": team})


@router.get("/my_band")
async def view_my_team(
        request: Request,
        user: User = Depends(get_user)
):
    team = await TeamDAO.get_my_team(user)
    return templates.TemplateResponse(name='my-band.html', context={"request": request, "team": team})


# API URls
@router.post('/create')
async def create_team(team_data: SchemaCreateTeam, capitan: User = Depends(get_user)):
    await TeamDAO.create_team(
        title=team_data.title,
        abbreviation=team_data.abbreviation,
        description=team_data.description,
        capitan=capitan.id,
    )

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=f"{team_data.title} успешно создана",
    )


@router.get('/my-team')
async def get_my_team(user: User = Depends(get_user)):
    team = await TeamDAO.get_my_team(user)
    return team
