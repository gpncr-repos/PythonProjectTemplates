from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from pydantic import PostgresDsn

from config import app_config
from interfaces import base_factory

app_config_ = app_config.app_config


class AlchemyEngineFactoryBase(base_factory.BaseFactory):
    """
    Базовая фабрика движка соединений для реализации Алхимии
    """

    _engine: Engine | AsyncEngine | None = None

    def __init__(self, dsn: PostgresDsn, max_size: int) -> None:
        """
        Инициализировать переменные
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        """

        self._dsn = dsn
        self._max_size = max_size

    @classmethod
    def _create(cls, dsn: PostgresDsn, max_size: int, **kwargs) -> Engine | AsyncEngine:
        """
        Создать единственный движок соединений
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        :return: объект движка соединений
        """

        raise NotImplementedError

    def create(self, **kwargs) -> Engine | AsyncEngine:
        """
        Создать движок соединений
        :return: объект движка соединений
        """

        return self._create(self._dsn, self._max_size, **kwargs)


class AlchemySyncEngineFactory(AlchemyEngineFactoryBase):
    """
    Фабрика синхронного движка соединений для реализации Алхимии
    """

    _engine: Engine | None = None

    @classmethod
    def _create(cls, dsn: PostgresDsn, max_size: int, **kwargs) -> Engine:
        """
        Создать единственный синхронный движок соединений
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        :return: объект синхронного движка соединений
        """

        if cls._engine is None:
            cls._engine = create_engine(
                str(dsn),
                pool_size=max_size,
                echo=True if app_config_.okd_stage == "DEV" else False,
                **kwargs
            )

        return cls._engine

    def create(self, **kwargs) -> Engine:
        """
        Создать синхронный движок соединений
        :return: объект синхронного движка соединений
        """

        return super().create(**kwargs)


class AlchemyAsyncEngineFactory(AlchemyEngineFactoryBase):
    """
    Фабрика асинхронного движка соединений для реализации Алхимии
    """

    _engine: AsyncEngine | None = None

    @classmethod
    def _create(cls, dsn: PostgresDsn, max_size: int, **kwargs) -> AsyncEngine:
        """
        Создать единственный асинхронный движок соединений
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        :return: объект асинхронного движка соединений
        """

        if cls._engine is None:
            cls._engine = create_async_engine(
                str(dsn),
                pool_size=max_size,
                echo=True if app_config_.okd_stage == "DEV" else False,
                **kwargs
            )

        return cls._engine

    def create(self, **kwargs) -> AsyncEngine:
        """
        Создать асинхронный движок соединений
        :return: объект асинхронного движка соединений
        """

        return super().create(**kwargs)