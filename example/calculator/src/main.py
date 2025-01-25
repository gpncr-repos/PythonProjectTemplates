import asyncio
import logging.config

from dependency_injector import providers

from config import logger_config
from interfaces import base_message_broker
from storage.raw_postgres.cursor_proxies import asyncpg_cursor_proxies
from tools.di_containers import rabbitmq_di_container, service_container, raw_postgres_container
from api import broker_api

logging.config.dictConfig(logger_config.get_json_output_logging_config())
logger = logging.getLogger("app")

consumer_container = rabbitmq_di_container.ConsumerContainer()
producer_container = rabbitmq_di_container.ProducerContainer()
oil_rate_service_container = service_container.ServiceContainer()
postgres_container = raw_postgres_container.AsyncpgContainer()

postgres_container.cursor_type.override(
    providers.Factory(asyncpg_cursor_proxies.ClientAsyncpgCursorProxy)
)

_consumer = consumer_container.consumer()
_producer = producer_container.producer()

event_loop = asyncio.get_event_loop()


async def serve(
    consumer: base_message_broker.BaseConsumer,
    producer: base_message_broker.BaseProducer,
) -> None:
    """
    Запустить консюмер сообщений
    :param consumer: консюмер команд на расчет
    :param producer: продюсер событий о конце расчета
    """

    logger.info("Приложение запущено")

    while True:
        await broker_api.consume(consumer, producer)


async def exit_app(
    consumer: base_message_broker.BaseConsumer,
    producer: base_message_broker.BaseProducer,
) -> None:
    """
    Завершить работу приложения
    :param consumer: консюмер команд на расчет
    :param producer: продюсер событий о конце расчета
    """

    logger.info("Отключение от брокера")
    await consumer.disconnect()
    await producer.disconnect()

    logger.info("Приложение остановлено")


if __name__ == "__main__":
    try:
        event_loop.run_until_complete(serve(_consumer, _producer))
    except KeyboardInterrupt:
        event_loop.run_until_complete(exit_app(_consumer, _producer))

        for task in asyncio.all_tasks(event_loop):
            task.cancel()
    finally:
        event_loop.close()
