from aiokafka import consumer as aio_consumer, producer as aio_producer
from pydantic import KafkaDsn

from config import kafka_config
from interfaces import base_proxy

config = kafka_config.config


class AsyncKafkaProducerProxy(base_proxy.ConnectionProxy):
    """
    Класс прокси-соединения для продюсера Kafka с реализацией aiokafka
    """

    def __init__(self, dsn: KafkaDsn = config.kafka_dsn) -> None:
        """
        Инициализировать переменные
        :param dsn: kafka dsn
        """

        self._dsn = dsn
        self._producer: aio_producer.AIOKafkaProducer | None = None

    async def connect(self) -> aio_producer.AIOKafkaProducer:
        """
        Подключиться к брокеру
        :return: объект продюсера
        """

        if self._producer is None:
            self._producer = aio_producer.AIOKafkaProducer(
                bootstrap_servers=str(self._dsn).removeprefix(f"{config.scheme}://")
            )

            await self._producer.start()

        return self._producer

    async def disconnect(self) -> None:
        """
        Отключиться от брокера
        """

        await self._producer.stop()


class AsyncKafkaConsumerProxy(base_proxy.ConnectionProxy):
    """
    Класс прокси-соединения для консюмера Kafka с реализацией aiokafka
    """

    def __init__(
        self,
        dsn: KafkaDsn = config.kafka_dsn,
        topic: str = config.topic,
        group_id: str | None = None,
    ) -> None:
        """
        Инициализировать переменные
        :param dsn: kafka dsn
        :param topic: название топика
        :param group_id: идентификатор группы консюмеров
        """

        self._dsn = dsn
        self._topic = topic
        self._group_id = group_id
        self._consumer: aio_consumer.AIOKafkaConsumer | None = None

    async def connect(self) -> aio_consumer.AIOKafkaConsumer:
        """
        Подключиться к брокеру
        :return: объект консюмера
        """

        if self._consumer is None:
            self._consumer = aio_consumer.AIOKafkaConsumer(
                self._topic,
                bootstrap_servers=str(self._dsn).removeprefix(f"{config.scheme}://"),
                auto_offset_reset="earliest",
                group_id=self._group_id,
            )

            await self._consumer.start()

        return self._consumer

    async def disconnect(self) -> None:
        """
        Отключиться от брокера
        """

        await self._consumer.stop()
