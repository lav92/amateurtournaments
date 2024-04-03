from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.users.router import router as user_router
from app.teams.router import router as team_router

app = FastAPI(
    title="Hello World",
)

templates = Jinja2Templates(directory='app/templates')

app.mount("/static", StaticFiles(directory="app/templates/static", html=True), name="static")

app.include_router(user_router)
app.include_router(team_router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name='home.html', context={"request": request})


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(name='login.html', context={"request": request})
