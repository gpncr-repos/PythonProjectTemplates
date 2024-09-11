import abc


class BaseSyncService(abc.ABC):
    """
    Базовый класс синхронного сервиса
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализировать переменные
        """

        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> any:
        """
        Выполнить логику сервиса
        """

        raise NotImplementedError


class BaseAsyncService(BaseSyncService, abc.ABC):
    """
    Базовый класс асинхронного сервиса
    """

    @abc.abstractmethod
    async def __call__(self, *args, **kwargs) -> any:
        """
        Выполнить логику сервиса
        """

        raise NotImplementedError
