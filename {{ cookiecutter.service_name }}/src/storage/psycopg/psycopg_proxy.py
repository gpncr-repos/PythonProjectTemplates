# thirdparty
import psycopg_pool

# project
from interfaces import base_postgres_cursor_proxy, base_proxy


class PsycopgConnectionProxy(base_proxy.ConnectionProxy):
    """
    Класс синхронного прокси-подключения с реализацией через psycopg
    """

    def __init__(
        self,
        connection_pool: psycopg_pool.ConnectionPool,
        cursor_proxy_type: type[base_postgres_cursor_proxy.BasePsycopgCursorProxy],
    ) -> None:
        """
        Инициализировать переменные
        :param connection_pool: пул соединений
        :param cursor_proxy_type: тип прокси для курсора
        """

        self._connection_pool = connection_pool
        self._cursor_proxy_type = cursor_proxy_type
        self._cursor: base_postgres_cursor_proxy.BasePsycopgCursorProxy | None = None

    def connect(self) -> base_postgres_cursor_proxy.BasePsycopgCursorProxy:
        """
        Подключиться к БД
        :return: объект соединения
        """

        if not self._cursor:
            connection = self._connection_pool.getconn()
            self._cursor = self._cursor_proxy_type(connection)

        return self._cursor

    def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        if not self._cursor:
            raise ValueError("Объект соединения не инициализирован")

        connection = self._cursor.cursor.connection
        self._cursor.cursor.close()
        self._connection_pool.putconn(connection)
        self._cursor = None


# class PsycopgAsyncConnectionProxy(base_proxy.ConnectionProxy):
#     """
#     Класс синхронного прокси-подключения с реализацией через psycopg
#     """
#
#     def __init__(self, db_config: PostgresConfig) -> None:
#         """
#         Инициализировать переменные
#         :param db_config: Конфиг БД
#         """
#         self._db_config = db_config
#         self._connection: psycopg.AsyncConnection | None = None
#         self._connection_users_count: int = 0
#
#     async def _set_connection(self) -> None:
#         """
#         Установить соединение
#         """
#
#         self._connection = await psycopg.AsyncConnection.connect(str(self._db_config.psycopg_dsn))
#
#     def _set_connection_users_count(self, new_count: int) -> None:
#         """
#         Установить число объектов, которые используют соединение
#         """
#
#         self._connection_users_count = new_count
#
#     async def connect(self) -> psycopg.AsyncConnection:
#         """
#         Подключиться к бд
#         :return: асинхронный объект соединения
#         """
#
#         self._set_connection_users_count(self._connection_users_count + 1)
#
#         if self._connection is None:
#             await self._set_connection()
#
#         return self._connection
#
#     async def disconnect(self) -> None:
#         """
#         Разорвать соединение
#         """
#
#         if self._connection is None:
#             raise ValueError("Объект соединения не инициализирован")
#
#         if self._connection_users_count > 0:
#             self._set_connection_users_count(self._connection_users_count - 1)
#
#         if self._connection_users_count == 0:
#             await self._connection.close()
#
#     async def commit(self):
#         """
#         Сделать коммит изменений
#         """
#         if self._connection is None:
#             raise ValueError("Объект соединения не инициализирован")
#
#         await self._connection.commit()
#
#     async def rollback(self) -> None:
#         """
#         Сделать откат изменений
#         """
#         if self._connection is None:
#             raise ValueError("Объект соединения не инициализирован")
#
#         await self._connection.rollback()
