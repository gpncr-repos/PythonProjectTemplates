import aio_pika

from config import rabbitmq_config
from interfaces import base_rabbitmq_routing_configurator as base_configurator

config = rabbitmq_config.config


class RoutingBuilder(base_configurator.BaseRoutingBuilder):
    """
    Класс Builder для создания маршрутизации сообщений
    """

    pass


class RoutingConfigurator(base_configurator.BaseRoutingConfiguratorMixin):
    """
    Класс-миксин, конфигурирующий обменники и очереди
    """

    _is_declared: bool = False

    async def configure_routes(self) -> None:
        """
        Сконфигурировать обменники и очереди, которые к ним привязаны
        """

        if self._is_declared is True:
            return

        exchange = await self._builder.declare_exchange(
            self._channel,
            config.exchange,
            aio_pika.ExchangeType.DIRECT
        )
        self._exchanges[exchange.name] = exchange

        queue = await self._builder.declare_queue(
            self._channel,
            config.queue
        )
        self._queues[queue.name] = queue

        await self._builder.bind_queue_to_exchange(queue, exchange, config.routing_key)

        self._is_declared = True
