from fastapi import APIRouter, HTTPException, status, Response

from app.users.schemas import SchemaRegisterUser
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация и авторизация']
)


@router.post('/register')
async def register_user(user_data: SchemaRegisterUser):
    print(user_data.__dict__)
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
