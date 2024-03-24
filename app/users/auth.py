from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
        Generates a password hash from the given password.
    """
    return pwd_context.hash(password)


def verify_password(in_password: str, hashed_password_db: str) -> bool:
    """
    Verifies a password hash.
    """
    return pwd_context.verify(in_password, hashed_password_db)


def create_access_token(data: dict) -> str:
    """
    Generates a JWT access token from the given data.
    """
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    data_copy.update({'exp': expire})
    encoded_jwt = jwt.encode(data_copy, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt
