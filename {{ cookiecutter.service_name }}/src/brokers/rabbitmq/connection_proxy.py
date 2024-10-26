import aio_pika

from config import rabbitmq_config
from interfaces import base_proxy

config = rabbitmq_config.config


class InstanceConnectionBase(base_proxy.ConnectionProxy):
    """
    Базовый класс прокси-подключения для разных сущностей с реализацией aio_pika
    """

    _connection: aio_pika.abc.AbstractRobustConnection | None = None
    _connection_users_count: int = 0

    @classmethod
    async def _set_connection(cls) -> None:
        """
        Установить соединение
        """

        cls._connection = await aio_pika.connect_robust(str(config.rabbit_mq_dsn))

    @classmethod
    def _set_connection_users_count(cls, new_count: int) -> None:
        """
        Установить число объектов, которые используют соединение
        """

        cls._connection_users_count = new_count

    async def connect(self) -> aio_pika.abc.AbstractRobustConnection:
        """
        Подключиться к брокеру
        :return: объект соединения
        """

        self._set_connection_users_count(self._connection_users_count + 1)

        if self._connection is None:
            await self._set_connection()

        return self._connection

    async def disconnect(self) -> None:
        """
        Отключиться от брокера
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        if self._connection_users_count > 0:
            self._set_connection_users_count(self._connection_users_count - 1)

        if self._connection_users_count == 0:
            await self._connection.close()


class AsyncRMQProducerConnectionProxy(InstanceConnectionBase):
    """
    Класс прокси-подключения для продюсера с реализацией aio_pika
    """

    pass


class AsyncRMQConsumerConnectionProxy(InstanceConnectionBase):
    """
    Класс прокси-подключения для консюмера с реализацией aio_pika
    """

    pass
