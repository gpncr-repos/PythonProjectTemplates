from dependency_injector import containers, providers

from brokers.kafka import consumer, producer


class ProducerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для продюсера
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    producer = providers.Factory(producer.KafkaProducer)


class ConsumerContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провадйерами для консюмера
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    consumer = providers.Factory(consumer.KafkaConsumer)
