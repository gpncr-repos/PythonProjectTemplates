# stdlib
import logging

# thirdparty
from aiokafka.errors import KafkaError

# project
from config import kafka_config
from interfaces import base_message_broker, base_proxy
from models.dto import broker_message_dto

logger = logging.getLogger(__name__)
config = kafka_config.config


class KafkaProducerAsync(base_message_broker.BaseProducer):
    """
    Класс Kafka producer, реализованный с помощью aiokafka
    """

    _connection_proxy: base_proxy.ConnectionProxy | None = None

    def __init__(
        self,
        connection_proxy: base_proxy.ConnectionProxy,
        topic: str = config.topic,
        model_type: type[
            broker_message_dto.BrokerMessageDTO
        ] = broker_message_dto.BrokerMessageDTO,
    ) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: объект прокси-соединения
        :param topic: название топика
        :param model_type: тип сообщения
        """

        self._connection_proxy = connection_proxy
        self._topic = topic
        self._model_type = model_type

    async def produce(self, message: broker_message_dto.BrokerMessageDTO) -> None:
        """
        Отправить сообщение в Kafka
        :param message: сообщение
        """

        if not isinstance(message, self._model_type):
            logger.error("Несоответствие типа сообщения; сообщение не отправлено")

            return

        producer = await self._connection_proxy.connect()

        try:
            payload = message.model_dump_json(by_alias=True).encode("utf-8")

            await producer.send(topic=self._topic, value=payload)
        except KafkaError:
            logger.exception(
                f"Не удалось отправить сообщение ({message.id} - {message.body} - {message.date}) в kafka"
            )

    async def disconnect(self) -> None:
        """
        Разорвать соединение с брокером
        """

        await self._connection_proxy.disconnect()
