from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend

# from redis import asyncio as aioredis

from app.users.router import router as user_router
from app.teams.router import router as team_router
from app.stats.router import router as stats_router
from app.templates.templates import templates
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO


app = FastAPI(
    title="Hello World",
)


app.mount("/static", StaticFiles(directory="app/templates/static", html=True), name="static")

app.include_router(user_router)
app.include_router(team_router)
app.include_router(stats_router)


@app.get("/", name="homepage")
async def root(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return templates.TemplateResponse(name='home.html', context={"request": request})
    else:
        user = await get_user(token=token)
        team = await TeamDAO.get_my_team(user)
    return templates.TemplateResponse(name='home.html', context={"request": request,
                                                                 "user": user,
                                                                 "team": team
                                                                 })


@app.get("/login", name="login")
async def login(request: Request):
    return templates.TemplateResponse(name='login.html', context={"request": request})


# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
