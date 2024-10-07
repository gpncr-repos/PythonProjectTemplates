import aio_pika

from brokers.rabbitmq import routing_configurator
from config import rabbitmq_config
from interfaces import base_message_broker, base_proxy, base_rabbitmq_routing_configurator as base_configurator
from models.dto import broker_message_dto

config = rabbitmq_config.config


class RabbitMQProducer(base_message_broker.BaseProducer, routing_configurator.RoutingConfigurator):
    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        builder: base_configurator.BaseRoutingBuilder,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: прокси-объект соединения
        :param builder: объект Builder для конфигурации маршрутизации
        :param model_type: тип сообщения
        """

        self._connection_proxy = connection_proxy
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.RobustChannel | None = None
        self._model_type = model_type

        super().__init__(builder)

    async def produce(self, exchange: str, routing_key: str, message: broker_message_dto.BrokerMessageDTO) -> None:
        """
        Отправить сообщение в обменник
        :param exchange: название обменника
        :param routing_key: ключ маршрутизации
        :param message: сообщение
        """

        if self._channel is None:
            raise ValueError("Объект канала не инициализирован")

        if not isinstance(message, self._model_type):
            raise ValueError("Несоответствие типа сообщения; сообщение не отправлено")

        message = aio_pika.Message(message.model_dump_json(by_alias=True).encode("utf-8"))

        await self._exchanges[config.exchange].publish(message, routing_key)

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
