# stdlib
from abc import ABC, abstractmethod


class BaseProducer(ABC):
    """Базовый интерфейс для асинхронного producer'а."""

    @abstractmethod
    async def produce(self, *args, **kwargs):
        """Produce метод."""

        raise NotImplementedError

    @abstractmethod
    async def start(self, *args, **kwargs):
        """Запустить асинхронный producer."""

        raise NotImplementedError

    @abstractmethod
    async def stop(self, *args, **kwargs):
        """Остановить асинхронный producer."""

        raise NotImplementedError
