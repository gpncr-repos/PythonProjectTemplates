# stdlib
import abc
from typing import Any

# thirdparty
from redis.asyncio import Redis




class RedisCacheRepository(abc.ABC):
    """
    Базовый класс для репозитория Redis
    """

    def __init__(self, connection: Redis) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        :param connection: подключение к Redis
        """

        self.connection = connection


class SetCacheMixin:
    """
    Миксин репозитория, содержащего метод set
    """

    @abc.abstractmethod
    def set(self, key, value: Any, *args, **kwargs) -> any:
        """
        Создать записи
        """

        raise NotImplementedError


class GetCacheMixin:
    """
    Миксин репозитория, содержащего метод get
    """

    @abc.abstractmethod
    def get(self, key, *args, **kwargs) -> any:
        """
        Получить записи
        """

        raise NotImplementedError



class DeleteCacheMixin:
    """
    Миксин репозитория, содержащего метод delete
    """

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> any:
        """
        Удалить записи
        """

        raise NotImplementedError