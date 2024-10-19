from __future__ import annotations  # no qa

# stdlib
import logging

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


class KafkaProducer(base_message_broker.BaseProducer):
    """
    Класс Kafka producer
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

        self._producer = AIOKafkaProducer(
            bootstrap_servers=str(dsn).removeprefix(config.scheme)
        )
        self._topic = topic
        self._model_type = model_type

    async def __aenter__(self) -> KafkaProducer:
        """
        Войти в контекстный менеджер
        :return: объект продюсера
        """

        await self._producer.start()

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Выйти из контекстного менеджера
        """

        pass

    async def produce(self, messages: list[broker_message_dto.BrokerMessageDTO]) -> None:
        """
         Отправить сообщения в Kafka
         :param messages: сообщения
         """

        for message in messages:
            if not isinstance(message, self._model_type):
                logger.error("Несоответствие типа сообщения; сообщение не отправлено")

                continue
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
