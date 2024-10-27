# thirdparty
import psycopg

# project
from config.pg_config import PostgresConfig


class PsycopgSyncConnection:
    """
    Класс синхронного соединения к Postgres, реализованный с помощью psycopg
    """

    def __init__(self, db_config: PostgresConfig) -> None:
        """
        Инициализация соединения с БД через psycopg

        :param db_config: Конфиг БД
        """
        self.db_config = db_config

    def get_connection(self) -> psycopg.Connection:
        """
        Получить соединение с БД
        """
        return psycopg.connect(str(self.db_config.psycopg_dsn))


class PsycopgAsyncConnection:
    """
    Класс асинхронного соединения к Postgres, реализованный с помощью psycopg
    """

    def __init__(self, db_config: PostgresConfig) -> None:
        """
        Инициализация асинхронного соединения с БД через psycopg

        :param db_config: Конфиг БД
        """
        self.db_config = db_config

    async def get_connection(self) -> psycopg.AsyncConnection:
        """
        Получить асинхронное соединение с БД
        """
        return await psycopg.AsyncConnection.connect(str(self.db_config.psycopg_dsn))
