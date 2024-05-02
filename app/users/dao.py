from fastapi import HTTPException, status

from app.dao.base import BaseDAO
from app.users.models import Users
from app.users.auth import get_password_hash


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def register_user(cls, email, password, first_name, last_name, nickname, steam_id):
        existing_user = await UsersDAO.find_or_none(email=email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже зарегистрирован"
            )
        hashed_password = get_password_hash(password)
        await UsersDAO.create(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            steam_id=int(steam_id),
        )
