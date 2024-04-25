from sqlalchemy import select, insert, update

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_or_none(cls, **params):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**params)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, pk_object: int, **data):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(id=pk_object).values(**data).returning(cls.model)
            updated_team = await session.execute(query)
            await session.commit()
            return updated_team.scalar_one_or_none()
