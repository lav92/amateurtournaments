from fastapi import APIRouter, HTTPException, status, Response, Depends, Form, Request

from app.users.schemas import SchemaRegisterUser, SchemaLoginUser
from app.users.dao import UsersDAO
from app.users.auth import verify_password, create_access_token
from app.users.models import User
from app.users.dependencies import get_user
from app.templates.templates import templates
from app.teams.dao import TeamDAO

router = APIRouter(
    prefix='',
    tags=['Аутентификация и авторизация']
)


# Frontend URLs
@router.post("/join")
async def join(
        request: Request,
        email: str = Form(),
        password: str = Form(),
        first_name: str = Form(),
        last_name: str = Form(),
        nickname: str = Form(),
        steam_id: str = Form(),
):
    await UsersDAO.register_user(email, password, first_name, last_name, nickname, steam_id)
    return templates.TemplateResponse(name='login.html', context={"request": request})


@router.post("/enter")
async def enter(
        request: Request,
        email: str = Form(),
        password: str = Form()
):
    user: User = await UsersDAO.find_or_none(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким email не зарегистрирован"
        )
    else:
        password_is_valid = verify_password(password, user.hashed_password)
        if not password_is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"
            )
    access_token = create_access_token({'sub': str(user.id)})
    response = templates.TemplateResponse(name='home.html', context={"request": request,
                                                                     "user": user,
                                                                     "team": await TeamDAO.get_my_team(user),
                                                                     })
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    return response


@router.get('/exit')
async def logout(request: Request):
    response = templates.TemplateResponse(name='home.html', context={"request": request})
    response.delete_cookie(key="access_token")
    return response


@router.get('/account')
async def account(request: Request, user: User = Depends(get_user)):
    return templates.TemplateResponse(name='account.html', context={"request": request,
                                                                    "user": user,
                                                                    "team": await TeamDAO.get_my_team(user),
                                                                    })


# API URLs
@router.post('/register')
async def register_user(user_data: SchemaRegisterUser):
    await UsersDAO.register_user(
        user_data.email,
        user_data.password,
        user_data.first_name,
        user_data.last_name,
        user_data.nickname
    )
    return Response(
        status_code=status.HTTP_201_CREATED,
        content="Пользователь успешно зарегистрирован"
    )


@router.post('/login')
async def login_user(response: Response, user_data: SchemaLoginUser):
    user: User = await UsersDAO.find_or_none(email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким email не зарегистрирован"
        )
    else:
        password_is_valid = verify_password(user_data.password, user.hashed_password)
        if not password_is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"
            )
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )
    return "Вы успешно авторизовались"


@router.post('/logout', name='logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')


@router.get('/account')
async def get_current_user(user: User = Depends(get_user)):
    return user.id, user.email, user.first_name, user.last_name, user.nickname
