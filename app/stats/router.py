from fastapi import APIRouter, Request, Depends, Form

from app.users.models import Users
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO
from app.stats.services import get_match_stats

from app.templates.templates import templates

router = APIRouter(
    prefix='',
    tags=['Статистика']
)


@router.get('/my_stats')
async def my_stats(request: Request, user: Users = Depends(get_user)):
    return templates.TemplateResponse(name='my_stats.html', context={"request": request,
                                                                     "user": user,
                                                                     "team": await TeamDAO.get_my_team(user),
                                                                     })


@router.post("/retrive_stats")
async def retrive_stats(
        request: Request,
        match_id: str = Form(),
        user: Users = Depends(get_user),
):

    await get_match_stats(user_id=user.id, match_id=match_id, steam_id=user.steam_id)
    return templates.TemplateResponse(name='home.html', context={"request": request,
                                                                 "user": user,
                                                                 "team": await TeamDAO.get_my_team(user),
                                                                 })
