from typing import Iterable

import psycopg
from config import app_config, pg_config
from interfaces import base_postgres_cursor_proxy

app_config = app_config.app_config
pg_config = pg_config.pg_config


class ClientPsycopgCursorProxy(base_postgres_cursor_proxy.BasePsycopgCursorProxy):
    """
    Прокси-класс для клиентского курсора psycopg
    """

    def init_cursor(self, connection: psycopg.Connection) -> None:
        """
        Инициализировать курсор
        :param connection: объект соединения
        """

        self.cursor = psycopg.ClientCursor(connection)

    def retrieve_many(
        self, sql_statement: str, rows_count: int, sql_params: dict | None = None
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

    def init_cursor(self, connection: psycopg.Connection) -> None:
        """
        Инициализировать курсор
        :param connection: объект соединения
        """

        self.cursor = psycopg.ServerCursor(
            connection, app_config.app_name + pg_config.cursor_name_salt
        )

    def retrieve_many(
        self, sql_statement: str, rows_count: int, sql_params: dict | None = None
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
