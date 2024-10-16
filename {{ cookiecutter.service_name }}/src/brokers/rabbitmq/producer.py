from __future__ import annotations  # no qa

import aio_pika

from config import rabbitmq_config
from interfaces import base_message_broker, base_proxy, base_rabbitmq_routing_configurator as base_configurator
from models.dto import broker_message_dto

config = rabbitmq_config.config


class RabbitMQProducer(base_message_broker.BaseProducer):
    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        router: base_configurator.BaseRoutingConfigurator,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: прокси-объект соединения
        :param router: конфигуратор маршрутизации сообщений
        :param model_type: тип сообщения
        """

        self._connection_proxy = connection_proxy
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._routing_configurator = router
        self._model_type = model_type
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None

    async def __aenter__(self) -> RabbitMQProducer:
        """
        Войти в контекстный менеджер
        :return: объект продюсера
        """

        self._connection = await self._connection_proxy.get_connection()
        self._channel = await self._connection.channel()

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        await self._channel.close()

    async def stop(self) -> None:
        """
        Остановить продюсер
        """

        await self._connection_proxy.close_connection()

    async def produce(
        self,
        exchange: str,
        routing_key: str,
        messages: list[broker_message_dto.BrokerMessageDTO]
    ) -> None:
        """
        Отправить сообщение в обменник
        :param exchange: название обменника
        :param routing_key: ключ маршрутизации
        :param messages: список сообщений
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        await self._routing_configurator.configure_routes(self._channel)

        for message in messages:
            if not isinstance(message, self._model_type):
                raise ValueError("Несоответствие типа сообщения; сообщение не отправлено")

            message = aio_pika.Message(message.model_dump_json(by_alias=True).encode("utf-8"))

            await self._routing_configurator.exchanges[config.exchange].publish(message, routing_key)
