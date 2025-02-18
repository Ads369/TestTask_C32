from typing import Union

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


async def init_db(engine: Union[Engine, AsyncEngine]):
    if isinstance(engine, AsyncEngine):
        async with engine.begin() as conn:
            # Uncomment the following line to drop all tables (useful in testing)
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    else:
        with engine.begin() as conn:
            # Uncomment the following line to drop all tables (useful in testing)
            # conn.run_sync(Base.metadata.drop_all)
            conn.run_sync(Base.metadata.create_all)
