from dependency_injector import containers, providers

from tools.factories import domain_factory, service_factory


class DomainContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами объектов доменной модели
    """

    geology_params_factory = providers.Factory(domain_factory.GeologyPropertiesFactory)
    well_factory = providers.Factory(domain_factory.WellFactory)
    cluster_factory = providers.Factory(domain_factory.ClusterFactory)


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами объектов сервисов
    """

    oil_rate_calc_service_factory = providers.Factory(service_factory.OilRateCalcServiceFactory)
