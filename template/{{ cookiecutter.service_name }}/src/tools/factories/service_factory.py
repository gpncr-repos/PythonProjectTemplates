from interfaces import base_factory
from models.dto import cluster_domain_dto
from services import oil_rate_calc_service


class OilRateCalcServiceFactory(base_factory.BaseFactory):
    """
    Фабрика объектов геологических свойств пласта
    """

    def create(
        self,
        geology_params: cluster_domain_dto.GeologyPropertiesDTO,
        wells: list[cluster_domain_dto.WellPropertiesDTO]
    ) -> oil_rate_calc_service.OilRateCalcService:
        """
        Создать объект сервиса расчета дебита куста скважин
        :param geology_params: геологические параметры
        :param wells: скважины
        :return: объект сервиса
        """

        return oil_rate_calc_service.OilRateCalcService(geology_params, wells)