from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastapi_demo.common.config import load_config

config = load_config()


def mk_db_url() -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        host=config.db.host,
        port=config.db.port,
        username=config.db.username,
        password=config.db.password,
        database=config.db.database
    )


engine = create_async_engine(mk_db_url(), pool_pre_ping=True)
SessionMaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session:
        yield session
