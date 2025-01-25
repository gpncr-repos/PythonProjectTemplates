from typing import Iterable

import asyncpg
from interfaces import base_postgres_cursor_proxy


class ClientAsyncpgCursorProxy(base_postgres_cursor_proxy.BaseAsyncpgCursorProxy):
    """
    Прокси-класс для клиентского курсора asyncpg
    """

    def init_cursor(self, connection: asyncpg.Connection) -> None:
        """
        Инициализировать курсор
        :param connection: объект соединения
        """

        self.cursor = connection

    async def retrieve_many(
        self, sql_statement: str, rows_count: int | None = None, sql_params: list | None = None
    ) -> Iterable[tuple]:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        result = await self.cursor.fetch(sql_statement, *sql_params)

        if rows_count:
            return result[:rows_count]

        return result


class ServerAsyncpgCursorProxy(base_postgres_cursor_proxy.BaseAsyncpgCursorProxy):
    """
    Прокси-класс для серверного курсора asyncpg
    """

    def init_cursor(self, connection: asyncpg.Connection) -> None:
        """
        Инициализировать курсор
        :param connection: объект соединения
        """

        self.cursor = connection

    async def retrieve_many(
        self, sql_statement: str, rows_count: int, sql_params: list | None = None
    ) -> Iterable[tuple]:
        """
        Получить записи из БД
        :param sql_statement: sql-запрос
        :param sql_params: значения для вставки в sql-запрос
        :param rows_count: количество строк для получения из БД
        """

        if sql_params:
            cursor = self.cursor.cursor(sql_statement, *sql_params, prefetch=rows_count)
        else:
            cursor = self.cursor.cursor(sql_statement, prefetch=rows_count)

        result = []
        row_number = 0

        async for row in cursor:
            result.append(row)
            row_number += 1

            if row_number == rows_count:
                yield result

                result = []
                row_number = 0

        yield result
