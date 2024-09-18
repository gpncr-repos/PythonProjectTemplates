# stdlib
from abc import ABC, abstractmethod


class BaseRepositoryAsync(ABC):
    """Базовый интерфейс для асинхронного клиента."""

    @abstractmethod
    async def create(self, *args, **kwargs):
        """Создать новый объект с заданными аргументами."""

        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, *args, **kwargs):
        """Получить объект на основе заданных аргументов."""

        raise NotImplementedError

    @abstractmethod
    async def retrieve_many(self, *args, **kwargs):
        """Получить несколько объектов на основе заданных аргументов."""

        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        """Обновить существующий объект заданными аргументами."""

        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """Удалить объект на основе заданных аргументов."""

        raise NotImplementedError
