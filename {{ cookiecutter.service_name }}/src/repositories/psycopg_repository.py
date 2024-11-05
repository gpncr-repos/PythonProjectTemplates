# stdlib
from typing import Any

from interfaces.base_raw_sql_creator import BaseRawSQLCreator

# project
from interfaces.base_repository import BaseRepository
from storage.psycopg.psycopg_connection import PsycopgAsyncConnection, PsycopgSyncConnection


class PsycopgSyncRepository(BaseRepository):
    """
    Синхронный репозиторий БД Postgres через соединение psycopg
    """

    def __init__(
        self,
        connection: PsycopgSyncConnection,
        sql_creator: BaseRawSQLCreator,
    ) -> None:
        """
        Инициализировать переменные
        :param connection: объект соединения psycopg
        :param sql_creator: объект класса для создания sql query
        """
        self._connection = connection
        self._sql_creator = sql_creator

    def create(self, table: str, data: dict[str, Any]) -> None:
        """
        Добавить запись в таблицу
        :param table: имя таблицы в бд
        :param data: словарь с данными для создания записи
        """
        insert_query = self._sql_creator.make_insert_query(table, list(data.keys()))
        with self._connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, list(data.values()))
                conn.commit()

    def retrieve(self, table: str, conditions: dict[str, Any]) -> tuple:
        """
        Получить запись из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        with self._connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_query, list(conditions.values()))
                return cursor.fetchone()

    def list(self, table: str, conditions: dict[str, Any] | None = None) -> list[tuple]:
        """
        Получить список записей из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        with self._connection.get_connection() as conn:
            with conn.cursor() as cursor:
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
        with self._connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_query, list(data.values()) + list(conditions.values()))
                conn.commit()

    def delete(self, table: str, conditions: dict[str, Any]) -> None:
        """
        Удалить записи из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для удаления
        """
        delete_query = self._sql_creator.make_delete_query(table, list(conditions.keys()))
        with self._connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_query, list(conditions.values()))
                conn.commit()


class PsycopgAsyncRepository(BaseRepository):
    """
    Acинхронный репозиторий БД Postgres через соединение psycopg
    """

    def __init__(
        self,
        connection: PsycopgAsyncConnection,
        sql_creator: BaseRawSQLCreator,
    ) -> None:
        """
        Инициализировать переменные
        :param connection: объект соединения psycopg
        :param sql_creator: объект класса для создания sql query
        """
        self._connection = connection
        self._sql_creator = sql_creator

    async def create(self, table: str, data: dict[str, Any]) -> None:
        """
        Добавить запись в таблицу
        :param table: имя таблицы в бд
        :param data: словарь с данными для создания записи
        """
        insert_query = self._sql_creator.make_insert_query(table, list(data.keys()))
        async with await self._connection.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(insert_query, list(data.values()))
                await conn.commit()

    async def retrieve(self, table: str, conditions: dict[str, Any]) -> tuple:
        """
        Получить запись из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        async with await self._connection.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(select_query, list(conditions.values()))
                return await cursor.fetchone()

    async def list(self, table: str, conditions: dict[str, Any] | None = None) -> list[tuple]:
        """
        Получить список записей из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для выборки
        """
        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        async with await self._connection.get_connection() as conn:
            async with conn.cursor() as cursor:
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
        async with await self._connection.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(update_query, list(data.values()) + list(conditions.values()))
                await conn.commit()

    async def delete(self, table: str, conditions: dict[str, Any]) -> None:
        """
        Удалить записи из таблицы
        :param table: имя таблицы в бд
        :param conditions: словарь с фильтрами для удаления
        """
        delete_query = self._sql_creator.make_delete_query(table, list(conditions.keys()))
        async with await self._connection.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(delete_query, list(conditions.values()))
                await conn.commit()
