# thirdparty
from dependency_injector import containers, providers

# project
from config import pg_config
from services import oil_rate_calc_service

config = pg_config.pg_config


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с сервисами
    """

    wiring_config = containers.WiringConfiguration(modules=["api.broker_api"])

    oil_rate_service = providers.Factory(oil_rate_calc_service.OilRateCalcService)
