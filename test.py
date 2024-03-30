import asyncio
from app.teams.models import Team
from app.teams.dao import TeamDAO

from app.users.models import User
from app.users.dao import UsersDAO

from app.database import async_session_maker
from sqlalchemy import select


async def test():
    user: User = await UsersDAO.find_or_none(id=10)
    team: Team = await TeamDAO.find_or_none(id=1)
    print(user.email, team.title)

    async with async_session_maker() as session:
        team.members = user
        query = select(Team).filter_by(id=1)
         

    print(type(async_session_maker))

asyncio.run(test())
