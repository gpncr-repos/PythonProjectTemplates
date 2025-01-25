import aio_pika
from config import rabbitmq_config
from interfaces import base_rabbitmq_routing_configurator as base_configurator

config = rabbitmq_config.config


class RoutingBuilder(base_configurator.BaseRoutingBuilder):
    """
    Класс Builder для создания маршрутизации сообщений/

    Экспериментальная реализация
    """

    pass


class RoutingConfigurator(base_configurator.BaseRoutingConfigurator):
    """
    Класс, конфигурирующий обменники и очереди.

    Экспериментальная реализация
    """

    _is_declared: bool = False

    @classmethod
    def _set_is_declared_to_true(cls) -> None:
        """
        Поставить значение переменной is_declared на True
        """
        cls._is_declared = True

    async def configure_routes(
        self, channel: aio_pika.abc.AbstractRobustChannel, *args, **kwargs
    ) -> None:
        """
        Сконфигурировать обменники и очереди, которые к ним привязаны
        :param channel: объект канала
        """

        if self._is_declared is True:
            return

        # Добавить свою реализацию маршрутизации

        exchange = await self._builder.declare_exchange(
            channel, config.exchange, aio_pika.ExchangeType.DIRECT
        )
        self.exchanges[exchange.name] = exchange

        command_queue = await self._builder.declare_queue(channel, config.command_queue)
        self.queues[command_queue.name] = command_queue

        event_queue = await self._builder.declare_queue(channel, config.event_queue)
        self.queues[event_queue.name] = event_queue

        await self._builder.bind_queue_to_exchange(command_queue, exchange, config.command_routing_key)
        await self._builder.bind_queue_to_exchange(event_queue, exchange, config.event_routing_key)

        self._set_is_declared_to_true()
