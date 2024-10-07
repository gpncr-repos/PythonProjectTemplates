import aio_pika

from config import rabbitmq_config
from interfaces import base_proxy

config = rabbitmq_config.config


class InstanceConnectionBase(base_proxy.ConnectionProxy):
    """
    Базовый класс подключения для разных сущностей
    """

    _connection: aio_pika.abc.AbstractRobustConnection | None = None

    @classmethod
    async def _set_connection(cls) -> None:
        """
        Установить соединение
        """

        cls._connection = await aio_pika.connect_robust(str(config.rabbit_mq_dsn))

    async def get_connection(self) -> aio_pika.abc.AbstractRobustConnection:
        """
        Получить соединение
        """

        if self._connection is None:
            await self._set_connection()

        return self._connection

    async def close_connection(self) -> None:
        """
        Закрыть соединение
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")
        else:
            await self._connection.close()


class ProducerConnection(InstanceConnectionBase):
    """
    Класс подключения для продюсера
    """

    pass


class ConsumerConnection(InstanceConnectionBase):
    """
    Класс подключения для консюмера
    """

    pass
