from __future__ import annotations  # no qa

import abc


class ConnectionProxy(abc.ABC):
    """
    Proxy для подключения к удаленным ресурсам
    """

    @abc.abstractmethod
    def get_connection(self) -> any:
        """
        Получить объект соединения
        """

        raise NotImplementedError

    @abc.abstractmethod
    def close_connection(self) -> None:
        """
        Закрыть соединение
        """

        raise NotImplementedError
