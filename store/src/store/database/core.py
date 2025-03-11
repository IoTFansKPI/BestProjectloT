import contextlib
from typing import AsyncIterator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from database.config import settings

Base = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = create_async_engine(
            DATABASE_URL,
            future=True,
            execution_options={
                "supports_sane_rowcount_returning": False,
                "supports_native_upsert": False,
            },
        )
        self._sessionmaker: async_sessionmaker | None = async_sessionmaker(
            autocommit=False, bind=self.engine
        )

    def init(self, host: str):
        self.engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()
        self._sessionmaker = None
        self.engine = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()


async def get_db():
    async with sessionmanager.session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db)]
