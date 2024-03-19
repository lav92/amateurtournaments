from sqlalchemy import select, insert

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
