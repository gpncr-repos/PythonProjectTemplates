from __future__ import annotations  # no qa

# stdlib
import logging
from contextlib import asynccontextmanager

# thirdparty
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from pydantic import KafkaDsn

# project
from config import kafka_config
from interfaces import base_message_broker
from models.dto import broker_message_dto

logger = logging.getLogger(__name__)
config = kafka_config.config


class KafkaProducerAsync(base_message_broker.BaseProducer):
    """
    Класс Kafka producer, реализованный с помощью aiokafka
    """

    def __init__(
        self,
        dsn: KafkaDsn = config.kafka_dsn,
        topic: str = config.topic,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Инициализировать переменные
        :param dsn: kafka dsn
        :param topic: название топика
        :param model_type: тип сообщения
        """

        self._producer: AIOKafkaProducer | None = None
        self._dsn = dsn
        self._topic = topic
        self._model_type = model_type

    @asynccontextmanager
    async def start(self) -> KafkaProducerAsync:
        """
        Запустить продюсера
        :return объект продюсера
        """

        self._producer = AIOKafkaProducer(
            bootstrap_servers=str(self._dsn).removeprefix(f"{config.scheme}://")
        )

        try:
            await self._producer.start()
        finally:
            yield self

    async def produce(self, message: broker_message_dto.BrokerMessageDTO) -> None:
        """
         Отправить сообщение в Kafka
         :param message: сообщение
         """

        if not isinstance(message, self._model_type):
            logger.error("Несоответствие типа сообщения; сообщение не отправлено")

            return

        try:
            payload = message.model_dump_json(by_alias=True).encode("utf-8")

            await self._producer.send(topic=self._topic, value=payload)
        except KafkaError:
            logger.exception(
                f"Не удалось отправить сообщение ({message.id} - {message.body} - {message.date}) в kafka"
            )

    async def stop(self) -> None:
        """
        Остановить продюсер Kafka
        """

        await self._producer.stop()
