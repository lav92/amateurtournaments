from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles

from app.users.router import router as user_router
from app.teams.router import router as team_router
from app.templates.templates import templates
from app.users.dependencies import get_user
from app.teams.dao import TeamDAO

app = FastAPI(
    title="Hello World",
)

# templates = Jinja2Templates(directory='app/templates')

app.mount("/static", StaticFiles(directory="app/templates/static", html=True), name="static")

app.include_router(user_router)
app.include_router(team_router)


@app.get("/", name="homepage")
async def root(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return templates.TemplateResponse(name='home.html', context={"request": request})
    else:
        user = await get_user(token=token)
    return templates.TemplateResponse(name='home.html', context={"request": request,
                                                                 "user": user,
                                                                 "team": await TeamDAO.get_my_team(user)
                                                                 })


@app.get("/login", name="login")
async def login(request: Request):
    return templates.TemplateResponse(name='login.html', context={"request": request})
