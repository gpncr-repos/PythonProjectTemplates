# thirdparty
import psycopg

# project
from config.pg_config import PostgresConfig
from interfaces import base_proxy


class PsycopgConnectionProxy(base_proxy.ConnectionProxy):
    """
    Класс синхронного прокси-подключения с реализацией через psycopg
    """

    def __init__(self, db_config: PostgresConfig) -> None:
        """
        Инициализировать переменные
        :param db_config: Конфиг БД
        """
        self._db_config = db_config
        self._connection: psycopg.Connection | None = None
        self._connection_users_count: int = 0

    def _set_connection(self) -> None:
        """
        Установить соединение
        """

        self._connection = psycopg.connect(str(self._db_config.psycopg_dsn))

    def _set_connection_users_count(self, new_count: int) -> None:
        """
        Установить число объектов, которые используют соединение
        """

        self._connection_users_count = new_count

    def connect(self) -> psycopg.Connection:
        """
        Подключиться к бд
        :return: объект соединения
        """

        self._set_connection_users_count(self._connection_users_count + 1)

        if self._connection is None:
            self._set_connection()

        return self._connection

    def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        if self._connection_users_count > 0:
            self._set_connection_users_count(self._connection_users_count - 1)

        if self._connection_users_count == 0:
            self._connection.close()

    def commit(self):
        """
        Сделать коммит изменений
        """
        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        self._connection.commit()

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """
        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        self._connection.rollback()


class PsycopgAsyncConnectionProxy(base_proxy.ConnectionProxy):
    """
    Класс синхронного прокси-подключения с реализацией через psycopg
    """

    def __init__(self, db_config: PostgresConfig) -> None:
        """
        Инициализировать переменные
        :param db_config: Конфиг БД
        """
        self._db_config = db_config
        self._connection: psycopg.AsyncConnection | None = None
        self._connection_users_count: int = 0

    async def _set_connection(self) -> None:
        """
        Установить соединение
        """

        self._connection = await psycopg.AsyncConnection.connect(str(self._db_config.psycopg_dsn))

    def _set_connection_users_count(self, new_count: int) -> None:
        """
        Установить число объектов, которые используют соединение
        """

        self._connection_users_count = new_count

    async def connect(self) -> psycopg.AsyncConnection:
        """
        Подключиться к бд
        :return: асинхронный объект соединения
        """

        self._set_connection_users_count(self._connection_users_count + 1)

        if self._connection is None:
            await self._set_connection()

        return self._connection

    async def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        if self._connection_users_count > 0:
            self._set_connection_users_count(self._connection_users_count - 1)

        if self._connection_users_count == 0:
            await self._connection.close()

    async def commit(self):
        """
        Сделать коммит изменений
        """
        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        await self._connection.commit()

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """
        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        await self._connection.rollback()
