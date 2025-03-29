from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
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
