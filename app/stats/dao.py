from app.dao.base import BaseDAO
from app.stats.models import Stats


class StatsDAO(BaseDAO):
    model = Stats
