# stdlib
import logging

# thirdparty
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from pydantic import KafkaDsn

# project
from interfaces.base_message_broker.produser import BaseProducer

logger = logging.getLogger(__name__)


class KafkaProducer(BaseProducer):
    """Асинхронный Kafka producer."""

    def __init__(self, dsn: KafkaDsn, topic: str, model_type: any) -> None:
        """Инициализация Kafka producer'а."""

        self.producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=dsn.unicode_string().removeprefix("kafka://")
        )
        self.topic: str = topic
        self.model_type: any = model_type

    async def produce(self, message: any):
        """Produce метод Kafka."""

        if not isinstance(message, self.model_type):
            logger.error("Несоответствие типа сообщения; сообщение не отправлено")
            return

        try:
            payload = message.model_dump_json(by_alias=True).encode("utf-8")
            await self.producer.send(topic=self.topic, value=payload)
        except KafkaError as e:
            logger.exception("Не удалось отправить сообщение в kafka")
            raise e

    async def start(self) -> None:
        """Запустить Kafka producer."""

        await self.producer.start()

    async def stop(self) -> None:
        """Остановить Kafka producer."""

        await self.producer.stop()
