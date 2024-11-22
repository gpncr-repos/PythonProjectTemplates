import psycopg_pool
from interfaces import base_factory
from pydantic import PostgresDsn


class PsycopgPoolFactory(base_factory.BaseFactory):
    """
    Фабрика пула соединений для реализации psycopg
    """

    _connection_pool: psycopg_pool.ConnectionPool | None = None

    def __init__(self, dsn: PostgresDsn, max_size: int) -> None:
        """
        Инициализировать переменные
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        """

        self._dsn = dsn
        self._max_size = max_size

    @classmethod
    def _create(cls, dsn: PostgresDsn, max_size: int) -> psycopg_pool.ConnectionPool:
        """
        Создать единственный пул соединений
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        :return: объект пула соединений
        """

        if cls._connection_pool is None:
            cls._connection_pool = psycopg_pool.ConnectionPool(str(dsn), max_size=max_size)

        return cls._connection_pool

    def create(self) -> psycopg_pool.ConnectionPool:
        """
        Создать пул соединений
        :return: объект пула соединений
        """

        return self._create(self._dsn, self._max_size)
