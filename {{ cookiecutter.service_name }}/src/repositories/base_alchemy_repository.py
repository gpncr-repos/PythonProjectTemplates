from typing import Iterable

from interfaces import base_repository
from storage.sqlalchemy import connection_proxy


class BaseAlchemyRepository(base_repository.BaseRepository):
    """
    Базовый класс репозитория для Алхимии
    """

    def __init__(self, connection_proxy_: connection_proxy.AlchemyConnectionProxyBase) -> None:
        """
        Инициализировать переменные
        :param connection_proxy_: объект прокси-соединения
        """

        self.connection_proxy = connection_proxy_

    def create(self, *args, **kwargs) -> None:
        """
        Создать запись
        """

        return super().create(*args, **kwargs)

    def retrieve(self, *args, **kwargs) -> any:
        """
        Получить запись
        """

        return super().retrieve(*args, **kwargs)

    def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    def update(self, *args, **kwargs) -> any:
        """
        Обновить запись
        """

        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs) -> any:
        """
        Удалить запись
        """

        return super().delete(*args, **kwargs)
