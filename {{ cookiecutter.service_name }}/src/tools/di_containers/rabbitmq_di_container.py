from dependency_injector import containers, providers

from brokers.rabbitmq import connection_proxy, consumer, producer, routing_configurator


class ProducerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для продюсера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    connection = providers.Factory(connection_proxy.AsyncRMQProducerConnectionProxy)
    producer = providers.Factory(producer.RabbitMQProducer, connection)


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    connection = providers.Factory(connection_proxy.AsyncRMQConsumerConnectionProxy)
    producer = providers.Factory(
        consumer.RabbitMQConsumer, connection, routing_configurator
    )
