# thirdparty
import asyncpg
import psycopg_pool

# project
from interfaces import base_postgres_cursor_proxy, base_proxy
from tools.factories import asyncpg_connection_pool_factory


class PsycopgConnectionProxy(base_proxy.ConnectionProxy):
    """
    Класс синхронного прокси-подключения с реализацией через psycopg
    """

    def __init__(
        self,
        connection_pool: psycopg_pool,
        cursor_proxy: base_postgres_cursor_proxy.BasePsycopgCursorProxy,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_pool: пул соединений
        :param cursor_proxy: прокси для курсора
        """

        self._connection_pool = connection_pool
        self._cursor_proxy = cursor_proxy

    def connect(self) -> base_postgres_cursor_proxy.BasePsycopgCursorProxy:
        """
        Подключиться к БД
        :return: объект соединения
        """

        if not self._cursor_proxy.cursor:
            connection = self._connection_pool.getconn()
            self._cursor_proxy.init_cursor(connection)

        return self._cursor_proxy

    def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        if not self._cursor_proxy:
            raise ValueError("Объект соединения не инициализирован")

        connection = self._cursor_proxy.cursor.connection
        self._cursor_proxy.cursor.close()
        self._connection_pool.putconn(connection)


class AsyncpgConnectionProxy(base_proxy.ConnectionProxy):
    """
    Класс синхронного прокси-подключения с реализацией через asyncpg
    """

    def __init__(
        self,
        connection_pool_factory: asyncpg_connection_pool_factory.AsyncpgPoolFactory,
        cursor_proxy: base_postgres_cursor_proxy.BaseAsyncpgCursorProxy,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_pool_factory: фабрика пулов соединений
        :param cursor_proxy: прокси для курсора
        """

        self._connection_pool_factory = connection_pool_factory
        self._cursor_proxy = cursor_proxy
        self._connection_pool: asyncpg.Pool | None = None

    async def connect(self) -> base_postgres_cursor_proxy.BaseAsyncpgCursorProxy:
        """
        Подключиться к БД
        :return: объект соединения
        """

        if self._connection_pool is None:
            self._connection_pool = await self._connection_pool_factory.create()

        if not self._cursor_proxy.cursor:
            connection = await self._connection_pool.acquire()
            self._cursor_proxy.init_cursor(connection)

        return self._cursor_proxy

    async def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        if not self._cursor_proxy:
            raise ValueError("Объект соединения не инициализирован")

        await self._connection_pool.release(self._cursor_proxy.cursor)
