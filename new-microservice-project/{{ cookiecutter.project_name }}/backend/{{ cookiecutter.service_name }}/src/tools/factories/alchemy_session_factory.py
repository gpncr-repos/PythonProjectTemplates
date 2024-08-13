# stdlib
from typing import AsyncGenerator, Optional, Generator

# thirdparty
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, Session

# project
from config import DBSettings


class AlchemySession:
    """
    Класс сессии sqlalchemy
    """

    def __init__(self, settings: DBSettings) -> None:
        """
        Инициализировать переменные
        """

        db_url = settings.pg_sync_dsn

        engine: Engine = create_engine(str(db_url), echo=True if settings.okd_stage == "DEV" else False)
        self.session_maker: Optional[sessionmaker] = sessionmaker(autocommit=False, bind=engine)

    def __call__(self) -> Generator[Session, None, None]:
        """
        Получить объект сессии
        :return: Объект сессии
        """

        if self.session_maker is None:
            raise ValueError("Объект создателя сессии не инициализирован")

        with self.session_maker() as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()


class AlchemyAsyncSession:
    """
    Класс асинхронной сессии sqlalchemy
    """

    def __init__(self, settings: DBSettings) -> None:
        """
        Инициализировать переменные
        """

        db_url = settings.pg_async_dsn

        engine: AsyncEngine = create_async_engine(str(db_url), echo=True if settings.okd_stage == "DEV" else False)
        self.session_maker: Optional[async_sessionmaker] = async_sessionmaker(autocommit=False, bind=engine)

    async def __call__(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Получить объект асинхронной сессии
        :return: Объект асинхронной сессии
        """

        if self.session_maker is None:
            raise ValueError("Объект создателя сессии не инициализирован")

        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
