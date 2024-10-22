from __future__ import annotations  # no qa

# stdlib
import json
import logging
from contextlib import asynccontextmanager

# thirdparty
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from pydantic import KafkaDsn, ValidationError


# project
from config import kafka_config
from interfaces import base_message_broker
from models.dto import broker_message_dto

logger = logging.getLogger(__name__)
config = kafka_config.config


class KafkaConsumerAsync(base_message_broker.BaseConsumer):
    """
    Класс Kafka consumer, реализованный с помощью aiokafka
    """

    def __init__(
        self,
        dsn: KafkaDsn = config.kafka_dsn,
        topic: str = config.topic,
        group_id: str | None = config.group,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Инициализировать переменные
        :param dsn: kafka dsn
        :param topic: название топика
        :param group_id: идентификатор группы консюмеров
        :param model_type: допустимый тип сообщения
        """

        self._consumer: AIOKafkaConsumer | None = None
        self._dsn = dsn
        self._topic = topic
        self._group_id = group_id
        self._model_type = model_type

    @asynccontextmanager
    async def start(self) -> KafkaConsumerAsync:
        """
        Запустить консюмера
        :return объект консюмера
        """

        self._consumer = AIOKafkaConsumer(
            self._topic,
            bootstrap_servers=str(self._dsn).removeprefix(f"{config.scheme}://"),
            auto_offset_reset="earliest",
            group_id=self._group_id
        )

        try:
            await self._consumer.start()
        finally:
            yield self

    async def retrieve(self) -> broker_message_dto.BrokerMessageDTO:
        """
        Прочитать одно сообщение из Kafka
        """

        try:
            message = await self._consumer.getone()
            payload = json.loads(message.value.decode("utf-8"))

            return self._model_type(**payload)
        except (ValidationError, KafkaError):
            logger.exception("Не удалось обработать сообщение из kafka")

    async def stop(self) -> None:
        """
        Остановить консюмера
        """

        await self._consumer.stop()
