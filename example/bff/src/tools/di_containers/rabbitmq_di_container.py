from brokers.rabbitmq import (
    connection_proxy,
    consumer,
    producer,
    routing_configurator
)
from dependency_injector import containers, providers


class ProducerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для продюсера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(packages=["services"])

    # указать свои типы соединений
    connection = providers.Singleton(connection_proxy.AsyncRMQProducerConnectionProxy)

    route_builder = providers.Factory(routing_configurator.RoutingBuilder)
    route_configurator = providers.Factory(routing_configurator.RoutingConfigurator, route_builder)

    producer = providers.Factory(producer.RabbitMQProducer, connection, route_configurator)


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(packages=[])

    # указать свои типы соединений
    connection = providers.Singleton(connection_proxy.AsyncRMQConsumerConnectionProxy)

    consumer = providers.Factory(consumer.RabbitMQConsumer, connection)
