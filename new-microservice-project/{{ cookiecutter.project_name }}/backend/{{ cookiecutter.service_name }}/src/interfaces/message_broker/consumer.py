# stdlib
from abc import ABC, abstractmethod


class BaseConsumer(ABC):
    """Базовый интерфейс для асинхронного consumer'а."""

    @abstractmethod
    async def consume(self, *args, **kwargs):
        """Consume метод."""

        raise NotImplementedError

    @abstractmethod
    async def start(self, *args, **kwargs):
        """Запустить асинхронный consumer."""

        raise NotImplementedError

    @abstractmethod
    async def stop(self, *args, **kwargs):
        """Остановить асинхронный consumer."""

        raise NotImplementedError
