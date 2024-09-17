from dependency_injector import containers, providers

from services import oil_rate_calc_service


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами объектов сервисов
    """

    wiring_config = containers.WiringConfiguration(modules=["web.entrypoints.oil_rate_calculator_entrypoint"])

    oil_rate_calc_service = providers.Factory(oil_rate_calc_service.OilRateCalcService)
