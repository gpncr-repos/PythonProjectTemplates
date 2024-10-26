import abc


class BaseProducer(abc.ABC):
    """
    Интерфейс для продюсера
    """

    @abc.abstractmethod
    async def produce(self, *args, **kwargs):
        """
        Отправить сообщение брокеру
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> any:
        """
        Разорвать соединение с брокером
        """

        raise NotImplementedError


class BaseConsumer(abc.ABC):
    """
    Интерфейс для асинхронного консюмера
    """

    @abc.abstractmethod
    async def retrieve(self, *args, **kwargs):
        """
        Прочитать одно сообщение из брокера
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> any:
        """
        Разорвать соединение с брокером
        """

        raise NotImplementedError
