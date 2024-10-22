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
    async def start(self, *args, **kwargs):
        """
        Запустить продюсер
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def stop(self, *args, **kwargs):
        """
        Остановить работу продюсера
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
    async def start(self, *args, **kwargs):
        """
        Запустить консюмера
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def stop(self, *args, **kwargs):
        """
        Остановить работу консюмера
        """

        raise NotImplementedError
