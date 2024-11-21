from __future__ import annotations  # no qa

import asyncpg.transaction

# project
from interfaces import base_postgres_cursor_proxy, base_uow
from repositories import asyncpg_repository


class AsyncpgUOW(base_uow.BaseSyncUOW):
    """
    Синхронный UOW для работы с синхронными Psycopg-репозиториями
    """

    def __init__(self, repository: asyncpg_repository.AsyncpgRepository) -> None:
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий Psycopg
        """

        self.repository = repository
        self._cursor_proxy: base_postgres_cursor_proxy.BaseAsyncpgCursorProxy | None = None
        self._transaction: asyncpg.transaction.Transaction | None = None
        self._is_transaction_commited = False
        super().__init__()

    async def __aenter__(self) -> AsyncpgUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        self._cursor_proxy = await self.repository.connection_proxy.connect()

        # возможность добавить свой уровень изоляции в аргумент isolation
        # в соответствии с документацией asyncpg
        self._transaction = self._cursor_proxy.cursor.transaction(isolation=None)
        await self._transaction.start()

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Сделать откат изменений
        """

        await self.rollback()

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        await self._transaction.commit()
        self._is_transaction_commited = True

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        if not self._is_transaction_commited:
            await self._transaction.rollback()

        await self.repository.connection_proxy.disconnect()
