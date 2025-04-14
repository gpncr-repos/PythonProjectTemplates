from __future__ import annotations  # noqa

from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from sqlalchemy.orm import SessionTransaction

from interfaces import base_uow
from repositories import base_alchemy_repository


class AlchemySyncUOW(base_uow.BaseAsyncUOW):
    """
    UOW для работы с синхронными репозиториями Алхимии
    """

    def __init__(
        self,
        repository: base_alchemy_repository.BaseAlchemyRepository
    ) -> None:
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий Алхимии
        """

        self._transaction: SessionTransaction | None = None
        self._is_transaction_commited = False

        self.repository = repository

    def __enter__(self) -> AlchemySyncUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        self._transaction = self.repository.connection_proxy.connect().begin()
        self._is_transaction_commited = False

        return self

    def __exit__(self, *args, **kwargs) -> None:
        """
        Сделать откат изменений
        """

        self.rollback()

    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        self._transaction.commit()
        self._is_transaction_commited = True

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        if not self._is_transaction_commited:
            self._transaction.rollback()

        self.repository.connection_proxy.disconnect()


class AlchemyAsyncUOW(base_uow.BaseAsyncUOW):
    """
    UOW для работы с асинхронными репозиториями Алхимии
    """

    def __init__(
        self,
        repository: base_alchemy_repository.BaseAlchemyRepository
    ) -> None:
        """
        Инициализировать переменные
        :param repository: асинхронный репозиторий Алхимии
        """

        self._transaction: AsyncSessionTransaction | None = None
        self._is_transaction_commited = False

        self.repository = repository

    async def __aenter__(self) -> AlchemyAsyncUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        self._transaction = await self.repository.connection_proxy.connect().begin()
        self._is_transaction_commited = False

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
