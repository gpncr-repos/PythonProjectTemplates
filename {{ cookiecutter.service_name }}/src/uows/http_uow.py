from interfaces import base_uow


class SyncHTTPUOW(base_uow.BaseSyncUOW):
    """
    Синхронный UOW для работы с синхронными HTTP-репозиториями
    """

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

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        super().commit()

    async def rollback(self) -> None:
        """
        Закрыть сессию
        """

        await self.repository.client.close()
