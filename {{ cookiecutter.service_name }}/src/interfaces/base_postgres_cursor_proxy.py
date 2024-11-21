import abc

import asyncpg
import psycopg


class BasePostgresCursorProxy(abc.ABC):
    """
    Базовый прокси-класс, позволяющий задать дополнительное поведение для курсора Postgres
    """

    @abc.abstractmethod
    def init_cursor(self, *args, **kwargs) -> None:
        """
        Инициализировать объект курсора
        """

        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_many(self, *args, **kwargs) -> any:
        """
        Получить записи из БД
        """

        raise NotImplementedError


class BasePsycopgCursorProxy(BasePostgresCursorProxy):
    """
    Базовый прокси-класс для курсора psycopg
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self.cursor: psycopg.Cursor | None = None

    def init_cursor(self, connection: psycopg.Connection) -> None:
        """
        Инициализировать курсор
        :param connection: объект соединения
        """

        super().init_cursor(connection)

    def retrieve_many(
        self, sql_statement: str, rows_count: int, sql_params: dict | None = None
    ) -> any:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        super().retrieve_many()


class BaseAsyncpgCursorProxy(BasePostgresCursorProxy):
    """
    Базовый прокси-класс для курсора asyncpg
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self.cursor: asyncpg.Connection | None = None

    def init_cursor(self, connection: asyncpg.Connection) -> None:
        """
        Инициализировать курсор
        :param connection: объект соединения
        """

        super().init_cursor(connection)

    async def retrieve_many(
        self, sql_statement: str, rows_count: int, sql_params: dict | None = None
    ) -> any:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        super().retrieve_many()
