# stdlib
from typing import Iterable

# project
from interfaces import base_postgres_cursor_proxy as cursor_proxy
from interfaces import base_proxy, base_raw_sql_creator, base_repository


class PsycopgSyncRepository(base_repository.BaseRepository):
    """
    Синхронный репозиторий БД Postgres через соединение psycopg
    """

    def __init__(
        self,
        connection_proxy_: base_proxy.ConnectionProxy,
        sql_creator: base_raw_sql_creator.BaseRawSQLCreator,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy_: прокси-объект соединения
        :param sql_creator: объект класса для создания запроса sql
        """

        self.connection_proxy = connection_proxy_
        self._sql_creator = sql_creator

    def _get_connection(self) -> cursor_proxy.BasePsycopgCursorProxy:
        """
        Получить курсор psycopg
        :return: объект курсора
        """

        return self.connection_proxy.connect()

    def create(self, table: str, data: dict[str, any]) -> None:
        """
        Добавить запись в таблицу
        :param table: имя таблицы в БД
        :param data: словарь с данными для создания записи
        """

        cursor = self._get_connection().cursor

        insert_query = self._sql_creator.make_insert_query(table, list(data.keys()))
        cursor.execute(insert_query, list(data.values()))

    def retrieve(self, table: str, conditions: dict[str, any]) -> tuple:
        """
        Получить запись из таблицы
        :param table: имя таблицы в БД
        :param conditions: словарь с фильтрами для выборки
        :return: запись из БД
        """

        cursor = self._get_connection().cursor

        select_query = self._sql_creator.make_select_query(table, list(conditions.keys()))
        cursor.execute(select_query, list(conditions.values()))

        return cursor.fetchone()

    def list(
        self, table: str, rows_count: int = 1000, conditions: dict[str, any] | None = None
    ) -> Iterable[tuple]:
        """
        Получить список записей из таблицы
        :param table: имя таблицы в БД
        :param rows_count: количество строк для получения из БД
        :param conditions: словарь с фильтрами для выборки
        :return: итерируемый объект, содержащий список записей
        """

        cursor = self._get_connection()

        sql_conditions = list(conditions.keys()) if conditions else None
        select_query = self._sql_creator.make_select_query(table, sql_conditions)
        sql_params = list(conditions.values()) if conditions else []

        return cursor.retrieve_many(select_query, sql_params, rows_count)

    def update(self, table: str, data: dict[str, any], conditions: dict[str, any]) -> None:
        """
        Обновить записи в таблице
        :param table: имя таблицы в БД
        :param data: словарь с данными для обновления записи
        :param conditions: словарь с фильтрами для выборки
        """

        cursor = self._get_connection().cursor

        update_query = self._sql_creator.make_update_query(
            table, list(data.keys()), list(conditions.keys())
        )
        cursor.execute(update_query, list(data.values()) + list(conditions.values()))

    def delete(self, table: str, conditions: dict[str, any]) -> None:
        """
        Удалить записи из таблицы
        :param table: имя таблицы в БД
        :param conditions: словарь с фильтрами для удаления
        """

        cursor = self._get_connection().cursor

        delete_query = self._sql_creator.make_delete_query(table, list(conditions.keys()))
        cursor.execute(delete_query, list(conditions.values()))
