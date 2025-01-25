import asyncio
import json

import aio_pika
from config import rabbitmq_config
from interfaces import (
    base_message_broker,
    base_proxy,
    base_rabbitmq_routing_configurator as routing_configurator
)
from models.dto import broker_message_dto

config = rabbitmq_config.config


class RabbitMQConsumer(base_message_broker.BaseConsumer):
    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        routing_configurator_: routing_configurator.BaseRoutingConfigurator,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: прокси-объект соединения
        :param routing_configurator_: конфигуратор маршрутизации сообщений
        """

        self._connection_proxy = connection_proxy
        self._routing_configurator = routing_configurator_
        self._queue: asyncio.Queue[aio_pika.abc.AbstractIncomingMessage] = asyncio.Queue()
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None

    async def retrieve(
        self, queue_name: str, prefetch_count: int = 1
    ) -> broker_message_dto.BrokerMessageDTO:
        """
        Прочитать сообщение из очереди
        :param queue_name: название очереди
        :param prefetch_count: количество сообщений, посылаемое брокером, за раз
        :return: прочитанное сообщение
        """

        connection = await self._connection_proxy.connect(self)

        if self._channel is None:
            self._channel = await connection.channel()

        await self._routing_configurator.configure_routes(self._channel)

        await self._channel.set_qos(prefetch_count=prefetch_count)

        queue = await self._channel.get_queue(queue_name)
        await queue.consume(self._queue.put)

        message = await self._queue.get()
        await message.ack()

        try:
            decoded = json.loads(message.body)
            return broker_message_dto.BrokerMessageDTO(
                id=decoded["id"], body=decoded["body"], date=decoded["date"]
            )
        except json.JSONDecodeError:
            raise

    async def disconnect(self) -> any:
        """
        Разорвать соединение с брокером
        """

        if self._channel:
            await self._channel.close()

        await self._connection_proxy.disconnect(self)
