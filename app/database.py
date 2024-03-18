from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'avl'
DB_PASSWORD = 'lav1907'
DB_NAME = 'tournaments'

DATABASE_URL = (f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
                f'/{DB_NAME}')

engine: AsyncEngine = create_async_engine(DATABASE_URL)

# параметр expire_on_commit=False не закрывает сессию после комита
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """
    класс Base используется для миграций
    """
    pass
