from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/front',
    tags=['frontend']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/')
async def hello(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request, "content": "pu pu pu"})
