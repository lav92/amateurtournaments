from typing import Optional

from pydantic import BaseModel, EmailStr


class SchemaRegisterUser(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None

