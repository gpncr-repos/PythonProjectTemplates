# stdlib
from typing import Union

# thirdparty
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

# project
from config.kafka_settings import KafkaSettings
from interfaces.message_broker import MessageBrokerInterface


class KafkaMessageBroker(MessageBrokerInterface):
    """Класс предоставляющий подключение к Kafka"""

    def __init__(
            self,
            producer: AIOKafkaProducer,
            consumers: dict[str, AIOKafkaConsumer],
            config: KafkaSettings,
    ) -> None:
        self.producer = producer
        self.consumers = consumers
        self.config = config

    async def startup_event(self):
        ...

    async def shutdown_event(self):
        ...

    async def consume(self, topic_name: str):
        ...

    async def produce(self, msg: Union[list, dict], topic_name: str, wait: bool = False):
        ...
