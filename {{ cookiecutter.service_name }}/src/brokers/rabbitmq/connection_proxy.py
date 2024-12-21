import aio_pika
from config import rabbitmq_config
from interfaces import base_message_broker, base_proxy

config = rabbitmq_config.config


class InstanceConnectionBase(base_proxy.ConnectionProxy):
    """
    Базовый класс прокси-подключения для разных сущностей с реализацией aio_pika
    """

    _connection: aio_pika.abc.AbstractRobustConnection | None = None
    _connection_users = set()

    @classmethod
    async def _set_connection(cls) -> None:
        """
        Установить соединение
        """

        cls._connection = await aio_pika.connect_robust(str(config.rabbit_mq_dsn))

    @classmethod
    def _add_connection_user(
        cls, new_user: base_message_broker.BaseConsumer | base_message_broker.BaseProducer
    ) -> None:
        """
        Установить число объектов, которые используют соединение
        :param new_user: новый пользователь
        """

        cls._connection_users.add(new_user)

    @classmethod
    def _delete_connection_user(
        cls, user: base_message_broker.BaseConsumer | base_message_broker.BaseProducer
    ) -> None:
        """
        Установить число объектов, которые используют соединение
        :param user: пользователь
        """

        cls._connection_users.remove(user)

    async def connect(
        self, user: base_message_broker.BaseConsumer | base_message_broker.BaseProducer
    ) -> aio_pika.abc.AbstractRobustConnection:
        """
        Подключиться к брокеру
        :param user: пользователь соединения
        :return: объект соединения
        """

        self._add_connection_user(user)

        if self._connection is None:
            await self._set_connection()

        return self._connection

    async def disconnect(
        self, user: base_message_broker.BaseConsumer | base_message_broker.BaseProducer
    ) -> None:
        """
        Отключиться от брокера
        :param user: пользователь соединения
        """

        if self._connection is None:
            raise ValueError("Объект соединения не инициализирован")

        self._delete_connection_user(user)

        if len(self._connection_users) == 0:
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
