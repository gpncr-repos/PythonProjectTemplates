from dependency_injector import containers, providers

from tools.factories import domain_factory


class DomainContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами объектов доменной модели
    """

    wiring_config = containers.WiringConfiguration(modules=["services.oil_rate_calc_service"])

    geology_params_factory = providers.Factory(domain_factory.GeologyPropertiesFactory)
    well_factory = providers.Factory(domain_factory.WellFactory)
    cluster_factory = providers.Factory(domain_factory.ClusterFactory)
