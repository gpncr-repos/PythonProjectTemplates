from __future__ import annotations  # no qa

# stdlib
import json
import logging

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


class KafkaConsumer(base_message_broker.BaseConsumer):
    """
    Класс Kafka consumer
    """

    def __init__(
        self,
        dsn: KafkaDsn = config.kafka_dsn,
        topics: str = config.topic,
        group_id: str | None = None,
        model_type: type[broker_message_dto.BrokerMessageDTO] = broker_message_dto.BrokerMessageDTO
    ) -> None:
        """
        Инициализировать переменные
        :param dsn: kafka dsn
        :param topics: список названий топиков
        :param group_id: идентификатор группы консюмеров
        :param model_type: допустимый тип сообщения
        """

        self._consumer = AIOKafkaConsumer(
            *topics, bootstrap_servers=str(dsn).removeprefix(config.scheme), group_id=group_id
        )
        self._model_type = model_type

    async def __aenter__(self) -> KafkaConsumer:
        """
        Войти в контекстный менеджер
        :return: объект консюмера
        """

        await self._consumer.start()

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        pass

    async def consume(self) -> broker_message_dto.BrokerMessageDTO:
        """
        Прочитать сообщение из Kafka
        """

        try:
            message = await self._consumer.getone()
            payload = json.loads(message.value.decode("utf-8"))
            result = self._model_type(**payload)
        except (ValidationError, KafkaError) as e:
            logger.exception("Не удалось обработать сообщение из kafka")
            raise e

        return result

    async def stop(self) -> None:
        """Остановить Kafka consumer."""

        await self._consumer.stop()
