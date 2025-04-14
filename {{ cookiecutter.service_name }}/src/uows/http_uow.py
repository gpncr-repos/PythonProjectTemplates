from interfaces import base_uow
from repositories import http_repository


class SyncHTTPUOW(base_uow.BaseSyncUOW):
    """
    Синхронный UOW для работы с синхронными HTTP-репозиториями
    """

    def __init__(self, repository: http_repository.SyncHTTPRepository):
        """
        Инициализировать переменные
        :param repository: синхронный репозиторий
        """

        self.repository = repository
        super().__init__()

    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        super().commit()

    def rollback(self) -> None:
        """
        Закрыть сессию
        """

        self.repository.client.close()


class AsyncHTTPUOW(base_uow.BaseAsyncUOW):
    """
    Асинхронный UOW для работы с асинхронными HTTP-репозиториями
    """

    def __init__(self, repository: http_repository.AsyncHTTPRepository):
        """
        Инициализировать переменные
        :param repository: асинхронный репозиторий
        """

        self.repository = repository
        super().__init__()

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        super().commit()

    async def rollback(self) -> None:
        """
        Закрыть сессию
        """

        await self.repository.client.aclose()
