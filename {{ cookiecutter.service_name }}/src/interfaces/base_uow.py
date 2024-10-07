from __future__ import annotations  # no qa

import abc

from interfaces import base_repository


class BaseSyncUOW(abc.ABC):
    """
    Абстрактный класс синхронного UOW для работы с синхронными репозиториями
    """

    def __init__(self, repository: base_repository.BaseRepository) -> None:
        """
        Инициализировать переменные
        :param repository: объект репозитория
        """

        self.repository = repository

    def __enter__(self, *args, **kwargs) -> BaseSyncUOW:
        """
        Войти в контекстный менеджер
        """

        return self

    def __exit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        raise NotImplementedError


class BaseAsyncUOW(BaseSyncUOW):
    """
    Абстрактный класс асинхронного UOW для работы с асинхронными репозиториями
    """

    async def __aenter__(self, *args, **kwargs) -> BaseAsyncUOW:
        """
        Войти в контекстный менеджер
        """

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        raise NotImplementedError
