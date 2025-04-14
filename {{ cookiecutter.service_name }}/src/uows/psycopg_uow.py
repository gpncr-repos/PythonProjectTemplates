from __future__ import annotations  # noqa

# project
from interfaces import base_postgres_cursor_proxy, base_uow
from repositories import psycopg_repository


class PsycopgSyncUOW(base_uow.BaseSyncUOW):
    """
    Синхронный UOW для работы с синхронными Psycopg-репозиториями
    """

    def __init__(self, repository: psycopg_repository.PsycopgSyncRepository) -> None:
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий Psycopg
        """

        self.repository = repository
        self._cursor_proxy: base_postgres_cursor_proxy.BasePsycopgCursorProxy | None = None
        super().__init__()

    def __enter__(self) -> PsycopgSyncUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        self._cursor_proxy = self.repository.connection_proxy.connect()

        return self

    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        self._cursor_proxy.cursor.connection.commit()

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        self._cursor_proxy.cursor.connection.rollback()
        self.repository.connection_proxy.disconnect()
