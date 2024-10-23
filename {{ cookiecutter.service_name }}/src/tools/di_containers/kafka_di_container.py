from dependency_injector import containers, providers

from brokers.kafka import connection_proxy, consumer, producer


class ProducerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для продюсера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    connection = providers.Factory(connection_proxy.AsyncKafkaProducerProxy)
    producer = providers.Factory(producer.KafkaProducerAsync, connection)


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    # указать модули, с которыми будет связан di-контейнер
    wiring_config = containers.WiringConfiguration(modules=None)

    connection = providers.Factory(connection_proxy.AsyncKafkaProducerProxy)
    consumer = providers.Factory(consumer.KafkaConsumerAsync, connection)
