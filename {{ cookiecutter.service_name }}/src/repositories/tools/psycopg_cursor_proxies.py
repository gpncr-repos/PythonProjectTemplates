from typing import Iterable

import psycopg
from interfaces import base_postgres_cursor_proxy
from psycopg import sql


class ClientPsycopgCursorProxy(base_postgres_cursor_proxy.BasePsycopgCursorProxy):
    """
    Прокси-класс для клиентского курсора psycopg
    """

    def __init__(self, connection: psycopg.Connection) -> None:
        """
        Инициализировать переменные
        :param connection: объект соединения
        """

        self.cursor = psycopg.ClientCursor(connection)
        super().__init__(connection)

    def retrieve_many(
        self, sql_statement: sql.SQL, sql_params: list[any], rows_count: int
    ) -> Iterable[tuple]:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        self.cursor.execute(sql_statement, sql_params)

        if rows_count:
            return self.cursor.fetchmany(rows_count)

        return self.cursor.fetchall()


class ServerPsycopgCursorProxy(base_postgres_cursor_proxy.BasePsycopgCursorProxy):
    """
    Прокси-класс для серверного курсора psycopg
    """

    def __init__(self, connection: psycopg.Connection) -> None:
        """
        Инициализировать переменные
        :param connection: объект соединения
        """

        self.cursor = psycopg.ServerCursor(connection, "test_cursor")
        super().__init__(connection)

    def retrieve_many(
        self, sql_statement: sql.SQL, sql_params: list[any], rows_count: int
    ) -> Iterable[tuple]:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        self.cursor.execute(sql_statement, sql_params)

        while rows := self.cursor.fetchmany(rows_count):
            if not rows:
                break

            yield rows
