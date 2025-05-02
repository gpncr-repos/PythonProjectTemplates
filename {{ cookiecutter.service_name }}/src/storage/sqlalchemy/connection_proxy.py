import asyncio
import time
from unittest.mock import MagicMock

from sqlalchemy import Engine, inspect, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session

from config import app_config, pg_config
from interfaces import base_proxy
from tools.factories import alchemy_engine_factory

app_config_ = app_config.app_config
pg_config_ = pg_config.pg_config


class AlchemyConnectionProxyBase(base_proxy.ConnectionProxy):
    """
    Базовое прокси-соединение для Алхимии
    """

    _session_maker: sessionmaker | None = None
    _session: Session | AsyncSession | None = None

    def __init__(
        self,
        engine_factory: alchemy_engine_factory.AlchemyEngineFactoryBase,
    ) -> None:
        """
        Инициализировать переменные
        """

        self._engine = engine_factory.create()

    def connect(self, *args, **kwargs) -> Session | AsyncSession:
        """
        Получить сессию БД
        :return: сессия
        """

        return super().connect(*args, **kwargs)

    def disconnect(self, *args, **kwargs) -> None:
        """
        Разорвать соединение с БД
        """

        super().disconnect(*args, **kwargs)


class AlchemySyncConnectionProxy(AlchemyConnectionProxyBase):
    """
    Синхронное прокси-соединение для Алхимии
    """

    _session_maker: sessionmaker | None = None
    _session: Session | None = None

    @classmethod
    def _connect(cls, engine: Engine) -> None:
        """
        Установить соединение с БД в рамках HTTP-сессии
        """

        if cls._session_maker is None:
            cls._session_maker = sessionmaker(  # noqa
                autocommit=False,
                autoflush=False,
                bind=engine,
                class_=Session,
                expire_on_commit=False,
            )

        if cls._session is None:
            cls._session = cls._session_maker()

    def connect(self) -> Session:
        """
        Получить сессию БД
        :return: асинхронная сессия
        """

        self._connect(self._engine)

        return self._session

    def disconnect(self) -> None:
        """
        Разорвать соединение с БД
        """

        if self._session:
            self._session.close()
            self._session = None

        self._session_maker = None


class AlchemyAsyncConnectionProxy(AlchemyConnectionProxyBase):
    """
    Асинхронное прокси-соединение для Алхимии
    """

    _session_maker: sessionmaker | None = None
    _session: AsyncSession | None = None

    @classmethod
    def _connect(cls, engine: AsyncEngine) -> None:
        """
        Установить соединение с БД в рамках HTTP-сессии
        """

        if cls._session_maker is None:
            cls._session_maker = sessionmaker(  # noqa
                autocommit=False,
                autoflush=False,
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

        if cls._session is None:
            cls._session = cls._session_maker()

    def connect(self) -> AsyncSession:
        """
        Получить сессию БД
        :return: асинхронная сессия
        """

        self._connect(self._engine)

        return self._session

    async def disconnect(self) -> None:
        """
        Разорвать соединение с БД
        """

        if self._session:
            await self._session.close()
            self._session = None

        self._session_maker = None


class AlchemyTestSyncConnectionProxy(AlchemyConnectionProxyBase):
    """
    Класс синхронного прокси-подключения для тестов
    """

    def __init__(
        self,
        engine_factory: alchemy_engine_factory.AlchemyEngineFactoryBase,
    ) -> None:
        """
        Инициализировать переменные
        """

        super().__init__(engine_factory)

        self._engine = create_engine(
            str(pg_config_.postgres_async_dsn),
            pool_size=pg_config_.connection_pool_size,
            echo=True
        )
        self._session_maker = sessionmaker(  # noqa
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            class_=Session,
            expire_on_commit=False,
        )

    def _mock(self):
        """
        Сделать моковое взаимодействие с БД
        """

        deletion = self._session.delete

        def mock_delete(instance):
            insp = inspect(instance)

            if not insp.persistent:
                self._session.expunge(instance)
            else:
                deletion(instance)

            return time.sleep(0)

        self._session.commit = MagicMock(side_effect=self._session.flush)
        self._session.delete = MagicMock(side_effect=mock_delete)

    def connect(self) -> AsyncSession:
        """
        Получить сессию БД
        :return: асинхронная сессия
        """

        self._session = self._session_maker()
        self._mock()

        return self._session

    def disconnect(self) -> None:
        """
        Разорвать соединение с БД
        """

        self._session.close()
        self._engine.dispose()


class AlchemyTestAsyncConnectionProxy(AlchemyConnectionProxyBase):
    """
    Класс асинхронного прокси-подключения для тестов
    """

    def __init__(
        self,
        engine_factory: alchemy_engine_factory.AlchemyEngineFactoryBase,
    ) -> None:
        """
        Инициализировать переменные
        """

        super().__init__(engine_factory)

        self._engine = create_async_engine(
            str(pg_config_.postgres_async_dsn),
            pool_size=pg_config_.connection_pool_size,
            echo=True
        )
        self._session_maker = sessionmaker(  # noqa
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    def _mock(self):
        """
        Сделать моковое взаимодействие с БД
        """

        deletion = self._session.delete

        async def mock_delete(instance):
            insp = inspect(instance)

            if not insp.persistent:
                self._session.expunge(instance)
            else:
                await deletion(instance)

            return await asyncio.sleep(0)

        self._session.commit = MagicMock(side_effect=self._session.flush)
        self._session.delete = MagicMock(side_effect=mock_delete)

    def connect(self) -> AsyncSession:
        """
        Получить сессию БД
        :return: асинхронная сессия
        """

        self._session = self._session_maker()
        self._mock()

        return self._session

    async def disconnect(self) -> None:
        """
        Разорвать соединение с БД
        """

        await self._session.close()
        await self._engine.dispose()
