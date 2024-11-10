# stdlib
from typing import Any

# project
from interfaces.base_raw_sql_creator import BaseRawSQLCreator
from interfaces.base_repository import BaseRepository
from storage.psycopg.psycopg_proxy import PsycopgAsyncConnectionProxy, PsycopgConnectionProxy


class PsycopgSyncRepository(BaseRepository):
    """
    Синхронный репозиторий БД Postgres через соединение psycopg
    """

    def __init__(
        self,
        connection_proxy: PsycopgConnectionProxy,
        sql_creator: BaseRawSQLCreator,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: объект прокси-соединения psycopg
        :param sql_creator: объект класса для создания sql query
        """
        self.connection_proxy = connection_proxy
        self._sql_creator = sql_creator

    def create(self, table: str, data: dict[str, Any]) -> None:
        """
        Добавить запись в таблицу
        :param table: имя таблицы в бд
        :param data: словарь с данными для создания записи
        """
        insert_query = self._sql_creator.make_insert_query(table, list(data.keys()))
        connection = self.connection_proxy.connect()
        with connection.cursor() as cursor:
            cursor.execute(insert_query, list(data.values()))

    def retrieve(self, table: str, conditions: dict[str, Any]) -> tuple:
        """
        Получить запись из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        connection = self.connection_proxy.connect()
        with connection.cursor() as cursor:
            cursor.execute(select_query, list(conditions.values()))
            return cursor.fetchone()

    def list(self, table: str, conditions: dict[str, Any] | None = None) -> list[tuple]:
        """
        Получить список записей из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        connection = self.connection_proxy.connect()
        with connection.cursor() as cursor:
            cursor.execute(select_query, list(conditions.values()))
            return cursor.fetchall()

    def update(self, table: str, data: dict[str, Any], conditions: dict[str, Any]) -> None:
        """
        Обновить записи в таблице
        :param table: имя таблицы в бд
        :param data: словарь с данными для обновления записи
        :param conditions: словарь с фильтрами для выборки
        """
        update_query = self._sql_creator.make_update_query(
            table, list(data.keys()), list(conditions.keys())
        )
        connection = self.connection_proxy.connect()
        with connection.cursor() as cursor:
            cursor.execute(update_query, list(data.values()) + list(conditions.values()))

    def delete(self, table: str, conditions: dict[str, Any]) -> None:
        """
        Удалить записи из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для удаления
        """
        delete_query = self._sql_creator.make_delete_query(table, list(conditions.keys()))
        connection = self.connection_proxy.connect()
        with connection.cursor() as cursor:
            cursor.execute(delete_query, list(conditions.values()))


class PsycopgAsyncRepository(BaseRepository):
    """
    Acинхронный репозиторий БД Postgres через соединение psycopg
    """

    def __init__(
        self,
        connection_proxy: PsycopgAsyncConnectionProxy,
        sql_creator: BaseRawSQLCreator,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: объект асинхронного прокси-соединения psycopg
        :param sql_creator: объект класса для создания sql query
        """
        self.connection_proxy = connection_proxy
        self._sql_creator = sql_creator

    async def create(self, table: str, data: dict[str, Any]) -> None:
        """
        Добавить запись в таблицу
        :param table: имя таблицы в бд
        :param data: словарь с данными для создания записи
        """
        insert_query = self._sql_creator.make_insert_query(table, list(data.keys()))
        connection = await self.connection_proxy.connect()
        async with connection.cursor() as cursor:
            await cursor.execute(insert_query, list(data.values()))

    async def retrieve(self, table: str, conditions: dict[str, Any]) -> tuple:
        """
        Получить запись из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        connection = await self.connection_proxy.connect()
        async with connection.cursor() as cursor:
            await cursor.execute(select_query, list(conditions.values()))
            return await cursor.fetchone()

    async def list(self, table: str, conditions: dict[str, Any] | None = None) -> list[tuple]:
        """
        Получить список записей из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        connection = await self.connection_proxy.connect()
        async with connection.cursor() as cursor:
            await cursor.execute(select_query, list(conditions.values()))
            return await cursor.fetchall()

    async def update(self, table: str, data: dict[str, Any], conditions: dict[str, Any]) -> None:
        """
        Обновить записи в таблице
        :param table: имя таблицы в бд
        :param data: словарь с данными для обновления записи
        :param conditions: словарь с фильтрами для выборки
        """
        update_query = self._sql_creator.make_update_query(
            table, list(data.keys()), list(conditions.keys())
        )
        connection = await self.connection_proxy.connect()
        async with connection.cursor() as cursor:
            await cursor.execute(update_query, list(data.values()) + list(conditions.values()))

    async def delete(self, table: str, conditions: dict[str, Any]) -> None:
        """
        Удалить записи из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для удаления
        """
        delete_query = self._sql_creator.make_delete_query(table, list(conditions.keys()))
        connection = await self.connection_proxy.connect()
        async with connection.cursor() as cursor:
            await cursor.execute(delete_query, list(conditions.values()))
