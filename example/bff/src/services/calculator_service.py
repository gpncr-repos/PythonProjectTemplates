import datetime
import logging
import uuid

from dependency_injector.wiring import inject, Provide

from config import rabbitmq_config
from interfaces import base_message_broker
from models.dto import broker_message_dto, eda_dto
from tools import enums
from tools.di_containers import rabbitmq_di_container

config = rabbitmq_config.config
logger = logging.getLogger(__name__)


class CalculatorService:
    """
    Сервис для работы с логикой расчета дебита куста скважин на заданный момент времени
    """

    @inject
    async def calculate(
        self,
        cluster_id: uuid.UUID,
        dt: datetime.datetime,
        producer: base_message_broker.BaseProducer = Provide[rabbitmq_di_container.ProducerContainer.producer]
    ) -> None:
        """
        Отправить команду на расчет
        :param cluster_id: идентификатор куста
        :param dt: дата замеров для расчета
        :param producer: продюсер команд на расчет
        """

        message = broker_message_dto.BrokerMessageDTO(
            body=dict(
                eda_dto.EDATypeDTO(
                    event_type=enums.CommandType.START_CALC.value,
                    cluster_id=cluster_id,
                    message="",
                    calc_date=dt
                )
            )
        )

        await producer.produce(config.exchange, config.command_routing_key, message)
        await producer.disconnect()
