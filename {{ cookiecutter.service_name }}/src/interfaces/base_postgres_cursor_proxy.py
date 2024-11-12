import abc

import psycopg
from psycopg import sql


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

    def retrieve_many(self, sql_statement: sql.SQL, sql_params: list[any], rows_count: int) -> any:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        super().retrieve_many()