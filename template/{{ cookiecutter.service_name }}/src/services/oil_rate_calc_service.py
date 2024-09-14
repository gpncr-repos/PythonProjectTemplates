from dependency_injector.wiring import Provide

from interfaces import base_service
from models.dto import cluster_domain_dto
from tools import di_container


class OilRateCalcService(base_service.BaseSyncService):
    """
    Сервис для работы с логикой расчета дебита куста скважин
    """

    geology_params_factory = Provide[
        di_container.DomainContainer.geology_params_factory
    ]
    well_factory = Provide[
        di_container.DomainContainer.well_factory
    ]
    cluster_factory = Provide[
        di_container.DomainContainer.cluster_factory
    ]

    def __init__(
        self,
        geology_params: cluster_domain_dto.GeologyPropertiesDTO,
        wells: list[cluster_domain_dto.WellPropertiesDTO]
    ) -> None:
        """
        Инициализировать переменные
        :param geology_params: геологические параметры
        :param wells: скважины
        """

        self.geology_params = geology_params
        self.wells = wells

    def calculate_cluster_oil_rate(self) -> float:
        """
        Выполнить логику расчета дебита куста скважин
        :return: дебит куста скважин
        """

        geology_params = self.geology_params_factory(self.geology_params)
        wells = [
            self.well_factory(well_params)
            for well_params in self.wells
        ]
        cluster = self.cluster_factory(geology_params)

        for well in wells:
            cluster.add_well(well)

        return cluster.calc_cluster_oil_rate()
