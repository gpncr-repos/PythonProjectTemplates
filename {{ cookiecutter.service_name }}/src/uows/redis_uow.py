from interfaces import base_uow
from repositories.redis_repository import AsyncRedisRepository, SyncRedisRepository


class SyncRedisUOW(base_uow.BaseSyncUOW):
    """
    Синхронный UOW для работы с синхронными Redis-репозиториями
    """

    def __init__(self, repository: SyncRedisRepository):
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий Redis
        """
        self.repository = repository
        super().__init__()

    def __exit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        self.repository.connection.close()

    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        super().commit()

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        super().rollback()


class AsyncRedisUOW(base_uow.BaseAsyncUOW):
    """
    Асинхронный UOW для работы с асинхронными Redis-репозиториями
    """

    def __init__(self, repository: AsyncRedisRepository):
        """
        Инициализировать переменные
        :param repository: асинхронный репозиторий Redis
        """
        self.repository = repository
        super().__init__()

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        await self.repository.connection.aclose()

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        super().commit()

    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        super().rollback()
