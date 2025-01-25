import datetime
import logging
import uuid

from dependency_injector.wiring import inject, Provide

from config import rabbitmq_config
from interfaces import base_uow
from models.dto import broker_message_dto, eda_dto
from tools import exceptions, enums
from tools.di_containers import raw_postgres_container

config = rabbitmq_config.config
logger = logging.getLogger(__name__)


class OilRateCalcService:
    """
    Сервис для работы с логикой расчета дебита куста скважин на заданный момент времени
    """

    @inject
    async def calc(
        self,
        root_id: uuid.UUID,
        dt: datetime.datetime,
        uow: base_uow.BaseAsyncUOW = Provide[
            raw_postgres_container.AsyncpgContainer.asyncpg_uow
        ]
    ) -> broker_message_dto.BrokerMessageDTO:
        """
        Выполнить логику расчета дебита куста скважин на текущий момент времени
        :param root_id: идентификатор агрегата Куст
        :param dt: дата замеров для расчета
        :param uow: uow для работы с репозиторием данных куста скважин
        """

        try:
            logger.info(f"Начало расчета.\nКуст: {root_id}, дата: {dt}")

            with uow:
                logger.info("Получение данных")
                cluster = await uow.repository.retrieve(root_id, dt)

                logger.info("Расчет дебита")
                oil_rate = cluster.calc_cluster_oil_rate()
        except Exception as e:
            logger.error(f"Произошла ошибка во время расчета: {e}")
            raise exceptions.CalcException("Произошла ошибка во время расчета")

        return broker_message_dto.BrokerMessageDTO(
            id=uuid.uuid4(),
            body=dict(
                eda_dto.EDATypeDTO(
                    event_type=enums.EventType.CALC_SUCCEED,
                    cluster_id=root_id,
                    message=str(oil_rate),
                    calc_date=dt
                )
            ),
            date=datetime.datetime.now()
        )
