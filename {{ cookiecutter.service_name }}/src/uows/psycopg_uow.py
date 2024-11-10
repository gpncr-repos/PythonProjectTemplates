# thirdparty
import psycopg

# project
from interfaces import base_uow
from repositories.psycopg_repository import PsycopgAsyncRepository, PsycopgSyncRepository


class PsycopgSyncUOW(base_uow.BaseSyncUOW):
    """
    Синхронный UOW для работы с синхронными Psycopg-репозиториями
    """

    def __init__(self, repository: PsycopgSyncRepository):
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий Psycopg
        """
        self.repository = repository
        super().__init__()

    def __exit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """
        try:
            self.commit()
        except psycopg.Error:
            self.rollback()

    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        self.repository.connection_proxy.commit()

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        self.repository.connection_proxy.rollback()
        self.repository.connection_proxy.disconnect()


class PsycopgAsyncUOW(base_uow.BaseAsyncUOW):
    """
    Acинхронный UOW для работы с aсинхронными Psycopg-репозиториями
    """

    def __init__(self, repository: PsycopgAsyncRepository):
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий Psycopg
        """
        self.repository = repository
        super().__init__()

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """
        try:
            await self.commit()
        except psycopg.Error:
            await self.rollback()

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        await self.repository.connection_proxy.commit()

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        await self.repository.connection_proxy.rollback()
        await self.repository.connection_proxy.disconnect()
