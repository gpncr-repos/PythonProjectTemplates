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
    wiring_config = containers.WiringConfiguration(modules=None)

    # указать свои типы соединений
    connection = providers.Singleton(connection_proxy.AsyncRMQProducerConnectionProxy)

    producer = providers.Factory(producer.RabbitMQProducer, connection)


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    # указать свои типы соединений
    connection = providers.Singleton(connection_proxy.AsyncRMQConsumerConnectionProxy)

    route_builder = providers.Factory(routing_configurator.RoutingBuilder)
    route_configurator = providers.Factory(routing_configurator.RoutingConfigurator, route_builder)

    consumer = providers.Factory(consumer.RabbitMQConsumer, connection, route_configurator)
