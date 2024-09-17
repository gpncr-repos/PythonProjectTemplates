from dependency_injector.wiring import Provide

from interfaces import base_service
from models.dto import cluster_domain_dto
from tools.di_containers import domain_di_container


class OilRateCalcService(base_service.BaseOilRateCalculatorService):
    """
    Сервис для работы с логикой расчета дебита куста скважин
    """

    geology_params_factory = Provide[
        domain_di_container.DomainContainer.geology_params_factory
    ]
    well_factory = Provide[
        domain_di_container.DomainContainer.well_factory
    ]
    cluster_factory = Provide[
        domain_di_container.DomainContainer.cluster_factory
    ]

    def calc_oil_rate(
        self,
        geology_params: cluster_domain_dto.GeologyPropertiesDTO,
        wells: list[cluster_domain_dto.WellPropertiesDTO]
    ) -> float:
        """
        Выполнить логику расчета дебита куста скважин
        :return: дебит куста скважин
        """

        geology_params = self.geology_params_factory.create(geology_params)
        wells = [
            self.well_factory.create(well_params)
            for well_params in wells
        ]
        cluster = self.cluster_factory.create(geology_params)

        for well in wells:
            cluster.add_well(well)

        return cluster.calc_cluster_oil_rate()
