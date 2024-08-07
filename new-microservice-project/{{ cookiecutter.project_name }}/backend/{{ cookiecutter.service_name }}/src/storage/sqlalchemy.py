from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from interfaces import ISqlAlchemy

from config import DBSettings
from functools import cached_property
from sqlalchemy import Engine


class SqlAlchemySync(ISqlAlchemy):
    def __init__(self, pg_settings: DBSettings) -> None:
        super().__init__(pg_settings)

    @cached_property
    def Session(self):  # noqa
        session_factory = sessionmaker(bind=self.__build_engine(), autocommit=False, autoflush=False)
        return scoped_session(session_factory)

    def get_db(self):
        db = self.Session()
        try:
            yield db
        finally:
            db.close()

    def __build_engine(self) -> Engine:
        return create_engine(self.pg_settings.pg_sync_dsn)


class SqlAlchemyAsync(ISqlAlchemy):
    def __init__(self, pg_settings: DBSettings) -> None:
        super().__init__(pg_settings)

    @cached_property
    def Session(self):  # noqa
        session_factory = sessionmaker(autocommit=False,  # noqa
                                       autoflush=False,
                                       bind=self.__build_engine(),
                                       class_=AsyncSession,
                                       expire_on_commit=False)
        return session_factory

    async def get_db(self):
        db = self.Session()
        try:
            yield db
        finally:
            await db.close()

    def __build_engine(self) -> AsyncEngine:
        return create_async_engine(self.pg_settings.pg_async_dsn)


Base = declarative_base()
