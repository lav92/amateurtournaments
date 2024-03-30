from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.schemas import SchemaRegisterUser, SchemaLoginUser
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, verify_password, create_access_token
from app.users.models import User
from app.users.dependencies import get_user

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация и авторизация']
)


@router.post('/register')
async def register_user(user_data: SchemaRegisterUser):
    existing_user = await UsersDAO.find_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.create(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        nickname=user_data.nickname,

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


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')


@router.get('/account')
async def get_current_user(user: User = Depends(get_user)):
    return user.id, user.email, user.first_name, user.last_name, user.nickname
