from dependency_injector import containers, providers

from tools.factories import service_factory


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами объектов сервисов
    """

    wiring_config = containers.WiringConfiguration(modules=["web.entrypoints.oil_rate_calculator_entrypoint"])

    oil_rate_calc_service_factory = providers.Factory(service_factory.OilRateCalcServiceFactory)
