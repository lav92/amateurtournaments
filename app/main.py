from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.users.router import router as user_router
from app.teams.router import router as team_router
from app.frontend.router import router as frontend_router

app = FastAPI(
    title="Hello World",
)

templates = Jinja2Templates(directory='app/templates')

app.mount("/static", StaticFiles(directory="app/templates/static", html=True), name="static")

app.include_router(user_router)
app.include_router(team_router)
app.include_router(frontend_router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name='index.html', context={"request": request})
