from typing import Optional

from pydantic import BaseModel, EmailStr


class SchemaRegisterUser(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None


class SchemaLoginUser(BaseModel):
    email: EmailStr
    password: str


class SchemaReturnUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    nickname: str
    steam_id: int
    role: str
