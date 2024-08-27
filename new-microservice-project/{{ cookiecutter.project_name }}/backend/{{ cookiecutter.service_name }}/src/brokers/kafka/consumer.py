# stdlib
import json
import logging
from typing import TypeVar

# thirdparty
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError
from pydantic import BaseModel, KafkaDsn, ValidationError


# project
from interfaces.message_broker.consumer import BaseConsumer


ConsumeModel = TypeVar("ConsumeModel", bound=BaseModel)

logger = logging.getLogger(__name__)


class KafkaConsumer(BaseConsumer):
    """Асинхронный Kafka consumer."""

    def __init__(self, dsn: KafkaDsn, topic: str) -> None:
        """Инициализация Kafka consumer'а."""

        self.consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            topic, bootstrap_servers=dsn.unicode_string().removeprefix("kafka://")
        )

    async def consume(self, model: type[ConsumeModel]) -> ConsumeModel:
        """Consume метод Kafka."""

        try:
            message = await self.consumer.getone()
            payload = json.loads(message.value.decode("utf-8"))
            result = model(**payload)
        except (ValidationError, KafkaError) as e:
            logger.exception("Не удалось обработать сообщение из kafka")
            raise e

        return result

    async def start(self) -> None:
        """Запустить Kafka consumer."""

        await self.consumer.start()

    async def stop(self) -> None:
        """Остановить Kafka consumer."""

        await self.consumer.stop()