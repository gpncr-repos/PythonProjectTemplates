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


class BaseAsyncService(BaseSyncService, abc.ABC):
    """
    Базовый класс асинхронного сервиса
    """

    pass
