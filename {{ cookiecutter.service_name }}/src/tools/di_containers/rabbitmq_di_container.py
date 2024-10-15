from dependency_injector import containers, providers

from brokers.rabbitmq import connections_manager, consumer, producer, routing_configurator


class ProducerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для продюсера
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    connection = providers.Factory(connections_manager.ProducerConnection)
    routing_builder = providers.Factory(routing_configurator.RoutingBuilder)
    routing_configurator = providers.Factory(routing_configurator.RoutingConfigurator, routing_builder)
    producer = providers.Factory(
        producer.RabbitMQProducer, connection, routing_configurator
    )


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    connection = providers.Factory(connections_manager.ConsumerConnection)
    routing_builder = providers.Factory(routing_configurator.RoutingBuilder)
    routing_configurator = providers.Factory(routing_configurator.RoutingConfigurator, routing_builder)
    producer = providers.Factory(
        consumer.RabbitMQConsumer, connection, routing_configurator
    )
