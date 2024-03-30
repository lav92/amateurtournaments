from pydantic import BaseModel
from typing import Optional


class SchemaCreateTeam(BaseModel):
    title: str
    abbreviation: str
    description: Optional[str] = None
