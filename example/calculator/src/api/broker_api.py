import datetime
import logging
import uuid

from dependency_injector.wiring import inject, Provide

from config import rabbitmq_config
from interfaces import base_message_broker
from models.dto import broker_message_dto, eda_dto
from tools import enums, exceptions
from tools.di_containers import rabbitmq_di_container, service_container

config = rabbitmq_config.config
logger = logging.getLogger(__name__)


@inject
async def consume(
    consumer: base_message_broker.BaseConsumer,
    producer: base_message_broker.BaseProducer,
    service = Provide[service_container.ServiceContainer.oil_rate_service]
) -> None:
    """
    Слушать события в брокере
    :param consumer: консюмер команд на расчет
    :param producer: продюсер событий о конце расчета
    :param service: сервис расчета
    """

    logger.info("Прослушивание очереди сообщений")

    try:
        message = await consumer.retrieve(config.command_queue)
        logger.info("Сообщение получено")

        event_data = eda_dto.EDATypeDTO(
            event_type=enums.CommandType(message.body["event_type"]),
            cluster_id=uuid.UUID(message.body["cluster_id"]),
            message=message.body["message"],
            calc_date=message.body["calc_date"],
        )

        await producer.produce(
            config.exchange,
            config.event_routing_key,
            broker_message_dto.BrokerMessageDTO(
                id=uuid.uuid4(),
                body=dict(
                    eda_dto.EDATypeDTO(
                        event_type=enums.EventType.CALC_STARTED,
                        cluster_id=event_data.cluster_id,
                        message="Расчет начат",
                        calc_date=message.body["calc_date"]
                    )
                ),
                date=datetime.datetime.now()
            )
        )

        return_message = await service.calc(
            event_data.cluster_id,
            datetime.datetime.strptime(message.body["calc_date"], "%Y-%m-%dT%H:%M:%S")
        )

        await producer.produce(config.exchange, config.event_routing_key, return_message)
    except exceptions.CalcException:
        await producer.produce(
            config.exchange,
            config.event_routing_key,
            broker_message_dto.BrokerMessageDTO(
                id=uuid.uuid4(),
                body=dict(
                    eda_dto.EDATypeDTO(
                        event_type=enums.EventType.CALC_FAILED,
                        cluster_id=event_data.cluster_id,
                        message="Расчет завершен с ошибкой",
                        calc_date=message.body["calc_date"]
                    )
                ),
                date=datetime.datetime.now()
            )
        )
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
