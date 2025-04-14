from brokers.rabbitmq import connection_proxy, consumer, producer
from dependency_injector import containers, providers


class ProducerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для продюсера
    """

    # Указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    # Указать свои типы соединений
    connection = providers.Singleton(connection_proxy.AsyncRMQProducerConnectionProxy)

    producer = providers.Factory(producer.RabbitMQProducer, connection)


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    # Указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    # Указать свои типы соединений
    connection = providers.Singleton(connection_proxy.AsyncRMQConsumerConnectionProxy)

    consumer = providers.Factory(consumer.RabbitMQConsumer, connection)
