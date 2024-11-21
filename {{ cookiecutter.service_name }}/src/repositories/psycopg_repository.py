# stdlib
from typing import Iterable

# project
from interfaces import base_postgres_cursor_proxy as cursor_proxy
from interfaces import base_repository
from storage.raw_postgres import connection_proxy


class PsycopgSyncRepository(base_repository.BaseRepository):
    """
    Синхронный репозиторий БД Postgres через соединение psycopg
    """

    def __init__(self, connection_proxy_: connection_proxy.PsycopgConnectionProxy) -> None:
        """
        Инициализировать переменные
        :param connection_proxy_: прокси-объект соединения
        """

        self.connection_proxy = connection_proxy_

    def _get_connection(self) -> cursor_proxy.BasePsycopgCursorProxy:
        """
        Получить курсор psycopg
        :return: объект курсора
        """

        return self.connection_proxy.connect()

    def _execute_query(self, query: str, params: dict | None = None) -> any:
        """
        Выполнить запрос
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        cursor = self._get_connection().cursor
        cursor.execute(query, params)

        return cursor

    def create(self, query: str, params: dict | None = None) -> None:
        """
        Добавить запись в таблицу
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        self._execute_query(query, params)

    def retrieve(self, query: str, params: dict | None = None) -> tuple:
        """
        Получить запись из таблицы
        :param query: запрос
        :param params: словарь с данными для создания записи
        :return: запись из БД
        """

        return self._execute_query(query, params).fetchone()

    def list(self, query: str, rows_count: int, params: dict | None = None) -> Iterable[tuple]:
        """
        Получить список записей из таблицы
        :param query: запрос
        :param params: словарь с данными для создания записи
        :param rows_count: количество строк для получения из БД
        :return: итерируемый объект, содержащий список записей
        """

        return self._execute_query(query, params).retrieve_many(query, rows_count, params)

    def update(self, query: str, params: dict | None = None) -> None:
        """
        Обновить записи в таблице
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        self._execute_query(query, params)

    def delete(self, query: str, params: dict | None = None) -> None:
        """
        Удалить записи из таблицы
        :param query: запрос
        :param params: словарь с данными для создания записи
        """

        self._execute_query(query, params)
