from datetime import datetime

from fastapi import HTTPException, Request, Depends, status
from jose import jwt, JWTError

from app.users.dao import UsersDAO
from app.config import settings


def get_token_auth_header(request: Request):
    """
    Returns the token from the Authorization header.
    """
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не найден",
        )
    return token


async def get_user(token: str = Depends(get_token_auth_header)):
    """
    Returns the user from JWT token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
        )

    expire: str = payload.get('exp')

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Время действия токена истекло",
        )

    user_id: int = payload.get('sub')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user = await UsersDAO.find_or_none(id=int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return user
