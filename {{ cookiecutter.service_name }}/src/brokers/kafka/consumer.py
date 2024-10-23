# stdlib
import json
import logging

# thirdparty
from aiokafka.errors import KafkaError
from pydantic import ValidationError


# project
from config import kafka_config
from interfaces import base_message_broker, base_proxy
from models.dto import broker_message_dto

logger = logging.getLogger(__name__)
config = kafka_config.config


class KafkaConsumerAsync(base_message_broker.BaseConsumer):
    """
    Класс Kafka consumer, реализованный с помощью aiokafka
    """

    _connection_proxy: base_proxy.ConnectionProxy | None = None

    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: объект прокси-соединения
        :param model_type: допустимый тип сообщения
        """

        self._connection_proxy = connection_proxy
        self._model_type = model_type

    async def retrieve(self) -> broker_message_dto.BrokerMessageDTO:
        """
        Прочитать одно сообщение из Kafka
        """

        consumer = await self._connection_proxy.connect()

        try:
            message = await consumer.getone()
            payload = json.loads(message.value.decode("utf-8"))

            return self._model_type(**payload)
        except (ValidationError, KafkaError):
            logger.exception("Не удалось обработать сообщение из kafka")

    async def disconnect(self) -> None:
        """
        Разорвать соединение с брокером
        """

        await self._connection_proxy.disconnect()
