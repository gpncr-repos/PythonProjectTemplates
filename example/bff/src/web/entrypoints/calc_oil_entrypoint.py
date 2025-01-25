import datetime
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query

from config import app_config
from tools.di_containers import service_container

router = APIRouter(tags=["calculator"])

app_config = app_config.app_config


@router.get("/calculate")
@inject
async def start_calc(
    calc_date: datetime.datetime = Query(alias="calcDate"),
    cluster_id: uuid.UUID = Query(alias="clusterId"),
    service = Provide[
        service_container.ServiceContainer.calculator_service
    ]
) -> None:
    """
    Начать расчет дебита нефти для куста на переданную дату
    :param calc_date: опорная дата
    :param cluster_id: идентификатор куста
    :param service: сервис расчета дебита нефти
    """

    await service.calculate(cluster_id, calc_date)
