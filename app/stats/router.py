from fastapi import APIRouter, Request, Depends, Form

from app.users.models import Users
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO
from app.stats.services import get_match_stats
from app.stats.dao import StatsDAO
from app.tasks.tasks import get_stats

from app.templates.templates import templates

router = APIRouter(
    prefix='',
    tags=['Статистика']
)


@router.get('/my_stats')
async def my_stats(request: Request, user: Users = Depends(get_user)):
    user_stats = await StatsDAO.find_all(user_id=user.id)
    return templates.TemplateResponse(name='my_stats.html', context={"request": request,
                                                                     "user": user,
                                                                     "team": await TeamDAO.get_my_team(user),
                                                                     "user_stats": user_stats,
                                                                     })


@router.post("/retrive_stats")
async def retrive_stats(
        request: Request,
        match_id: str = Form(),
        user: Users = Depends(get_user),
):
    get_stats.delay(user_id=user.id, match_id=match_id, steam_id=user.steam_id, user_email=user.email)
    return templates.TemplateResponse(name='home.html', context={"request": request,
                                                                 "user": user,
                                                                 "team": await TeamDAO.get_my_team(user),
                                                                 })
