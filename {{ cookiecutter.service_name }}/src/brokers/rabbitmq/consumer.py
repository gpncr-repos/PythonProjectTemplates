from __future__ import annotations  # no qa

import asyncio
import json

import aio_pika

from config import rabbitmq_config
from interfaces import base_message_broker, base_proxy, base_rabbitmq_routing_configurator as base_configurator
from models.dto import broker_message_dto

config = rabbitmq_config.config


class RabbitMQConsumer(base_message_broker.BaseConsumer):
    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        router: base_configurator.BaseRoutingConfigurator
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: прокси-объект соединения
        :param router: конфигуратор маршрутизации сообщений
        """

        self._connection_proxy = connection_proxy
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._routing_configurator = router
        self._queue: asyncio.Queue[aio_pika.abc.AbstractIncomingMessage] = asyncio.Queue()
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None

    async def __aenter__(self, prefetch_count: int = 1) -> RabbitMQConsumer:
        """
        Войти в контекстный менеджер
        :param prefetch_count: количество сообщений, посылаемое брокером, за раз
        :return: объект продюсера
        """

        self._connection = await self._connection_proxy.get_connection()
        self._channel = await self._connection.channel()

        await self._routing_configurator.configure_routes(self._channel)
        await self._channel.set_qos(prefetch_count=prefetch_count)

        await self._routing_configurator.queues[config.queue].consume(self._queue.put)

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        await self._channel.close()
        await self._connection_proxy.close_connection()

    async def consume(self, queue: str) -> broker_message_dto.BrokerMessageDTO:
        """
        Прочитать сообщение из очереди
        :param queue: название очереди
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        message = await self._queue.get()
        await message.ack()

        try:
            decoded = json.loads(message.body)
            return broker_message_dto.BrokerMessageDTO(
                id=decoded["id"],
                body=decoded["body"],
                date=decoded["date"]
            )
        except json.JSONDecodeError:
            raise
