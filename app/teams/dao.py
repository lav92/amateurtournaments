from app.dao.base import BaseDAO
from app.teams.models import Team


class TeamDAO(BaseDAO):
    model = Team
