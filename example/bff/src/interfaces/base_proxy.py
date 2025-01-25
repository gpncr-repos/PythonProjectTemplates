import abc


class ConnectionProxy(abc.ABC):
    """
    Proxy для подключения к удаленным ресурсам
    """

    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> any:
        """
        Подключиться к ресурсу
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> any:
        """
        Отключиться от ресурса
        """

        raise NotImplementedError
