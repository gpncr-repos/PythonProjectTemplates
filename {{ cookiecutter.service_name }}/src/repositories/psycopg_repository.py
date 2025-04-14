# stdlib
import abc
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

    def _execute_query(self, query: str, params: list | None = None) -> any:
        """
        Выполнить запрос
        :param query: запрос
        :param params: список с параметрами запроса
        """

        cursor = self._get_connection().cursor
        cursor.execute(query, params)

        return cursor

    @abc.abstractmethod
    def create(self, *args, **kwargs) -> any:
        """
        Добавить запись в таблицу
        """

        return super().create(*args, **kwargs)

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs) -> any:
        """
        Получить запись из таблицы
        """

        return super().retrieve(*args, **kwargs)

    @abc.abstractmethod
    def update(self, *args, **kwargs) -> any:
        """
        Обновить записи в таблице
        """

        return super().update(*args, **kwargs)

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> any:
        """
        Удалить записи из таблицы
        """

        return super().delete(*args, **kwargs)

    def list(self, query: str, rows_count: int, params: list | None = None) -> Iterable[tuple]:
        """
        Получить список записей из таблицы
        :param query: запрос
        :param params: список с параметрами запроса
        :param rows_count: количество строк для получения из БД
        :return: итерируемый объект, содержащий список записей
        """

        connection = self._get_connection()

        return connection.retrieve_many(query, rows_count, params)
