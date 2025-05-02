from __future__ import annotations  # noqa

from unittest.mock import MagicMock

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


class TestAlchemySyncUOW(AlchemySyncUOW):
    """
    Тестовый UOW для асинхронной реализации Алхимии
    """

    def __init__(self, repository: base_alchemy_repository.BaseAlchemyRepository):
        """
        Инициализировать переменные
        :param repository: репозиторий
        """

        super().__init__(repository)

        self._session = self.repository.connection_proxy.connect()
        self.repository.connection_proxy.connect = MagicMock(side_effect=lambda: self._session)

    def __enter__(self) -> TestAlchemySyncUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        return self

    def __exit__(self, *args, **kwargs) -> None:
        """
        Сделать откат изменений
        """

        pass

    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        self._session.commit()

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        self._session.rollback()
        self.repository.connection_proxy.disconnect()


class TestAlchemyAsyncUOW(AlchemyAsyncUOW):
    """
    Тестовый UOW для асинхронной реализации Алхимии
    """

    def __init__(self, repository: base_alchemy_repository.BaseAlchemyRepository):
        """
        Инициализировать переменные
        :param repository: репозиторий
        """

        super().__init__(repository)

        self._session = self.repository.connection_proxy.connect()
        self.repository.connection_proxy.connect = MagicMock(side_effect=lambda: self._session)

    async def __aenter__(self) -> TestAlchemyAsyncUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Сделать откат изменений
        """

        pass

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        await self._session.commit()

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        await self._session.rollback()
        await self.repository.connection_proxy.disconnect()
