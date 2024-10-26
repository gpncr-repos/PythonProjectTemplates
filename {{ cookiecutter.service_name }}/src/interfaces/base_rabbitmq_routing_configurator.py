import abc

import aio_pika


class BaseRoutingBuilder:
    """
    Базовый класc конфигуратора маршрутизации сообщений для RabbitMQ (aio_pika), реализующий паттерн Builder.
    Является объектом Builder.

    Экспериментальный интерфейс для задания маршрутизации сообщений в коде
    """

    async def declare_exchange(
        self,
        channel: aio_pika.abc.AbstractRobustChannel,
        name: str,
        type_: aio_pika.ExchangeType,
        *args,
        **kwargs
    ) -> aio_pika.abc.AbstractRobustExchange:
        """
        Объявить обменник сообщениями
        :param channel: объект канала
        :param name: название обменника сообщениями
        :param type_: тип обменника сообщениями
        :return: объект обменника сообщениями
        """

        return await channel.declare_exchange(name, type_, *args, **kwargs)

    async def declare_queue(
        self,
        channel: aio_pika.abc.AbstractRobustChannel,
        name: str,
        *args,
        **kwargs
    ) -> aio_pika.abc.AbstractRobustQueue:
        """
        Объявить обменник сообщениями
        :param channel: объект канала
        :param name: название очереди
        :return: объект очереди
        """

        return await channel.declare_queue(name, *args, **kwargs)

    async def bind_queue_to_exchange(
        self,
        queue: aio_pika.abc.AbstractRobustQueue,
        exchange: aio_pika.abc.AbstractRobustExchange,
        routing_key: str | None = None,
        *args,
        **kwargs
    ) -> None:
        """
        Связать очередь с обменником сообщений
        :param queue: объект очереди
        :param exchange: объект обменника сообщениями
        :param routing_key: ключ маршрутизации
        """

        await queue.bind(exchange, routing_key, *args, **kwargs)

    async def bind_exchange_to_exchange(
        self,
        exchange: aio_pika.abc.AbstractRobustExchange,
        exchange_to_bind: aio_pika.abc.AbstractRobustExchange,
        routing_key: str | None = None,
        *args,
        **kwargs
    ) -> None:
        """
        Связать обменник сообщений с другим обменником
        :param exchange: объект обменника сообщениями
        :param exchange_to_bind: объект обменника сообщениями для связывания
        :param routing_key: ключ маршрутизации
        """

        await exchange.bind(exchange_to_bind, routing_key, *args, **kwargs)


class BaseRoutingConfigurator(abc.ABC):
    """
    Базовый класс конфигуратора маршрутизации сообщений для RabbitMQ (aio_pika), реализующий паттерн Builder.
    Является объектом Director.

    Экспериментальный интерфейс для задания маршрутизации сообщений в коде
    """

    def __init__(self, builder: BaseRoutingBuilder) -> None:
        """
        Инициализировать переменные
        :param builder: объект Builder, предоставляющий методы для конфигурирования маршрутов
        """

        self._builder = builder
        self.exchanges: dict[str, aio_pika.abc.AbstractRobustExchange] = {}
        self.queues: dict[str, aio_pika.abc.AbstractRobustQueue] = {}

    async def get_exchange(
        self,
        name: str,
        channel: aio_pika.abc.AbstractRobustChannel
    ) -> aio_pika.abc.AbstractExchange:
        """
        Получить объект обменника сообщений по его названию
        :param name: название обменника сообщениями
        :param channel: объект канала
        :return: объект обменника сообщениями
        """

        if name not in self.exchanges:
            raise ValueError("Обменник сообщений с таким именем не зарегистрирован")

        return await channel.get_exchange(name)

    async def get_queue(
        self,
        name: str,
        channel: aio_pika.abc.AbstractRobustChannel
    ) -> aio_pika.abc.AbstractQueue:
        """
        Получить объект очереди по ее названию
        :param name: название очереди
        :param channel: объект канала
        :return: объект очереди
        """

        if name not in self.queues:
            raise ValueError("Очередь с таким именем не зарегистрирована")

        return await channel.get_queue(name)

    @abc.abstractmethod
    async def configure_routes(self, channel: aio_pika.abc.AbstractRobustChannel, *args, **kwargs) -> None:
        """
        Сконфигурировать маршрутизацию сообщений
        :param channel: объект канала
        """

        raise NotImplementedError
