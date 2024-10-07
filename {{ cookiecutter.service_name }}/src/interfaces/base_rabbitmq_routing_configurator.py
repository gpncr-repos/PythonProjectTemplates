import abc

import aio_pika


class BaseRoutingBuilder(abc.ABC):
    """
    Базовый класc конфигуратора маршрутизации сообщений для RabbitMQ, реализующий паттерн Builder.
    Является объектом Builder
    """

    async def declare_exchange(
        self,
        channel: aio_pika.RobustChannel,
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

    async def declare_queue(self, channel: aio_pika.RobustChannel, name: str) -> aio_pika.abc.AbstractRobustQueue:
        """
        Объявить обменник сообщениями
        :param channel: объект канала
        :param name: название очереди
        :return: объект очереди
        """

        return await channel.declare_queue(name)

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


class BaseRoutingConfiguratorMixin(abc.ABC):
    """
    Базовый класc-миксин конфигуратора маршрутизации сообщений для RabbitMQ, реализующий паттерн Builder.
    Является объектом Director.
    Поле _channel должно быть инициализировано в наследуемом классе
    """

    _channel: aio_pika.RobustChannel

    def __init__(self, builder: BaseRoutingBuilder) -> None:
        """
        Инициализировать переменные
        :param builder: объект Builder, предоставляющий методы для конфигурирования маршрутов
        """

        self._builder = builder
        self._exchanges: dict[str, aio_pika.abc.AbstractRobustExchange] = {}
        self._queues: dict[str, aio_pika.abc.AbstractRobustQueue] = {}

    @abc.abstractmethod
    async def configure_routes(self, *args, **kwargs) -> None:
        """
        Сконфигурировать маршрутизацию сообщений
        """

        raise NotImplementedError
