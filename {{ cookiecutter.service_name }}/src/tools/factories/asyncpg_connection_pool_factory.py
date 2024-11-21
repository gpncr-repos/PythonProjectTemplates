import asyncpg
from interfaces import base_factory
from pydantic import PostgresDsn


class AsyncpgPoolFactory(base_factory.BaseFactory):
    """
    Фабрика пула соединений для реализации asyncpg
    """

    _connection_pool: asyncpg.Pool | None = None

    def __init__(self, dsn: PostgresDsn, max_size: int) -> None:
        """
        Инициализировать переменные
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        """

        self._dsn = dsn
        self._max_size = max_size

    @classmethod
    async def _create(cls, dsn: PostgresDsn, max_size: int) -> asyncpg.Pool:
        """
        Создать единственный пул соединений
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        :return: объект пула соединений
        """

        if cls._connection_pool is None:
            cls._connection_pool = await asyncpg.create_pool(str(dsn), max_size=max_size)

        return cls._connection_pool

    async def create(self) -> asyncpg.Pool:
        """
        Создать пул соединений
        :return: объект пула соединений
        """

        return await self._create(self._dsn, self._max_size)
