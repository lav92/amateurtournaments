from fastapi import APIRouter, Depends, status, Response, Request, Form

from app.teams.schemas import SchemaCreateTeam
from app.users.models import User
from app.users.dao import UsersDAO
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
        capitan=capitan,
    )

    return templates.TemplateResponse(name='home.html', context={"request": request,
                                                                 "team": team,
                                                                 "user": capitan,
                                                                 })


@router.get("/my_band")
async def view_my_team(
        request: Request,
        user: User = Depends(get_user)
):
    team = await TeamDAO.get_my_team(user)
    print(team.capitan)
    print(type(team.capitan))
    return templates.TemplateResponse(name='my-band.html', context={"request": request,
                                                                    "team": team,
                                                                    "user": user,
                                                                    })


@router.post("/invite_carry")
async def invite_carry(
        request: Request,
        carry_email: str = Form(),
        user: User = Depends(get_user)
):
    carry: User = await UsersDAO.find_or_none(email=carry_email)
    team = await TeamDAO.get_my_team(user)
    updated_team = await TeamDAO.update(pk_object=team.id, mid=carry.id)
    return templates.TemplateResponse(name='my-band.html', context={"request": request,
                                                                    "team": updated_team,
                                                                    "user": user,
                                                                    })


@router.post("/invite_mid")
async def invite_mid(
        request: Request,
        mid_email: str = Form(),
        user: User = Depends(get_user)
):
    mid: User = await UsersDAO.find_or_none(email=mid_email)
    team = await TeamDAO.get_my_team(user)
    updated_team = await TeamDAO.update(pk_object=team.id, mid=mid.id)
    return templates.TemplateResponse(name='my-band.html', context={"request": request,
                                                                    "team": updated_team,
                                                                    "user": user,
                                                                    })


@router.post("/invite_offlane")
async def invite_offlane(
        request: Request,
        offlane_email: str = Form(),
        user: User = Depends(get_user)
):
    invited_user: User = await UsersDAO.find_or_none(email=offlane_email)
    team = await TeamDAO.get_my_team(user)
    updated_team = await TeamDAO.update(pk_object=team.id, offlane=invited_user.id)
    return templates.TemplateResponse(name='my-band.html', context={"request": request,
                                                                    "team": updated_team,
                                                                    "user": user,
                                                                    })


@router.post("/invite_support")
async def invite_support(
        request: Request,
        support_email: str = Form(),
        user: User = Depends(get_user)
):
    invited_user: User = await UsersDAO.find_or_none(email=support_email)
    team = await TeamDAO.get_my_team(user)
    updated_team = await TeamDAO.update(pk_object=team.id, support=invited_user.id)
    return templates.TemplateResponse(name='my-band.html', context={"request": request,
                                                                    "team": updated_team,
                                                                    "user": user,
                                                                    })


@router.post("/invite_hard_support")
async def invite_hard_support(
        request: Request,
        hard_support_email: str = Form(),
        user: User = Depends(get_user)
):
    invited_user: User = await UsersDAO.find_or_none(email=hard_support_email)
    team = await TeamDAO.get_my_team(user)
    updated_team = await TeamDAO.update(pk_object=team.id, hard_support=invited_user.id)
    return templates.TemplateResponse(name='my-band.html', context={"request": request,
                                                                    "team": updated_team,
                                                                    "user": user,
                                                                    })


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
