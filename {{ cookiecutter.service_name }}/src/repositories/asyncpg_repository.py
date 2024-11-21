# stdlib
from typing import Iterable

# project
from interfaces import base_postgres_cursor_proxy as cursor_proxy
from interfaces import base_repository
from storage.raw_postgres import connection_proxy


class AsyncpgRepository(base_repository.BaseRepository):
    """
    Синхронный репозиторий БД Postgres через соединение asyncpg
    """

    def __init__(self, connection_proxy_: connection_proxy.AsyncpgConnectionProxy) -> None:
        """
        Инициализировать переменные
        :param connection_proxy_: прокси-объект соединения
        """

        self.connection_proxy = connection_proxy_

    async def _get_connection(self) -> cursor_proxy.BaseAsyncpgCursorProxy:
        """
        Получить курсор psycopg
        :return: объект курсора
        """

        return await self.connection_proxy.connect()

    async def _execute_query(self, query: str, params: dict | None = None) -> any:
        """
        Выполнить запрос с параметрами
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        connection = await self._get_connection()
        cursor = connection.cursor

        if not params:
            await cursor.execute(query)
        else:
            await cursor.execute(query, params)

        return cursor

    async def create(self, query: str, params: dict | None = None) -> None:
        """
        Добавить запись в таблицу
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        await self._execute_query(query, params)

    async def retrieve(self, query: str, params: dict | None = None) -> tuple:
        """
        Получить запись из таблицы
        :param query: запрос
        :param params: словарь с данными для создания записи
        :return: запись из БД
        """

        connection = await self._get_connection()
        cursor = connection.cursor

        return await cursor.fetchrow(query, params)

    async def list(
        self, query: str, rows_count: int, params: dict | None = None
    ) -> Iterable[tuple]:
        """
        Получить список записей из таблицы
        :param query: запрос
        :param params: словарь с данными для создания записи
        :param rows_count: количество строк для получения из БД
        :return: итерируемый объект, содержащий список записей
        """

        connection = await self._get_connection()

        return connection.retrieve_many(query, rows_count, params)

    async def update(self, query: str, params: dict | None = None) -> None:
        """
        Обновить записи в таблице
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        await self._execute_query(query, params)

    async def delete(self, query: str, params: dict | None = None) -> None:
        """
        Удалить записи из таблицы
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        await self._execute_query(query, params)
