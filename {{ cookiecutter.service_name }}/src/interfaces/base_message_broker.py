# stdlib
from abc import ABC, abstractmethod


class BaseProducer(ABC):
    """Базовый интерфейс для асинхронного producer'а."""

    @abstractmethod
    async def produce(self, *args, **kwargs):
        """Produce метод."""

        raise NotImplementedError

    @abstractmethod
    async def stop(self, *args, **kwargs):
        """Остарновить работу продюсера"""

        raise NotImplementedError


class BaseConsumer(ABC):
    """Базовый интерфейс для асинхронного consumer'а."""

    @abstractmethod
    async def consume(self, *args, **kwargs):
        """Consume метод."""

        raise NotImplementedError

    @abstractmethod
    async def stop(self, *args, **kwargs):
        """Остарновить работу консюмера"""

        raise NotImplementedError
