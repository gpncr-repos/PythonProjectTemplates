from typing import Callable

import aio_pika

from brokers.rabbitmq import routing_configurator
from config import rabbitmq_config
from interfaces import base_message_broker, base_proxy, base_rabbitmq_routing_configurator as base_configurator

config = rabbitmq_config.config


class RabbitMQConsumer(base_message_broker.BaseConsumer, routing_configurator.RoutingConfigurator):
    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        builder: base_configurator.BaseRoutingBuilder
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: прокси-объект соединения
        :param builder: объект Builder для конфигурации маршрутизации
        """

        self._connection_proxy = connection_proxy
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.RobustChannel | None = None

        super().__init__(builder)

    async def consume(
        self,
        queue: str,
        callback_func: Callable[..., any],
        prefetch_count: int = 1
    ) -> None:
        """
        Прочитать сообщение из очереди
        :param queue: название очереди
        :param callback_func: функция-обработчик сообщения
        :param prefetch_count: количество сообщений, посылаемое брокером, за раз
        """

        if self._channel is None:
            raise ValueError("Объект канала не инициализирован")

        await self._channel.set_qos(prefetch_count=prefetch_count)

        await self._queues[config.queue].consume(callback_func)

    async def start(self) -> None:
        """
        Запустить продюсер
        """

        self._connection = await self._connection_proxy.get_connection()
        self._channel = await self._connection.channel()
        await self.configure_routes()

    async def stop(self) -> None:
        """
        Остановить продюсер
        """

        if self._channel is None:
            raise ValueError("Объект канала не инициализирован")

        await self._channel.close()
