from fastapi import APIRouter, Request, Depends

from app.users.models import User
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO

from app.templates.templates import templates

router = APIRouter(
    prefix='',
    tags=['Статистика']
)


@router.get('/my_stats')
async def my_stats(request: Request, user: User = Depends(get_user)):
    return templates.TemplateResponse(name='my_stats.html', context={"request": request,
                                                                     "user": user,
                                                                     "team": await TeamDAO.get_my_team(user),
                                                                     })


@router.post("/retrive_stats")
async def retrive_stats(request: Request, user: User = Depends(get_user)):
    return templates.TemplateResponse(name='home.html', context={"request": request,
                                                                 "user": user,
                                                                 "team": await TeamDAO.get_my_team(user),
                                                                 })
