import uuid

from interfaces import base_domain_model as domain
from models.domain.cluster import entities, value_objects


class Cluster(domain.DomainAggregate):
    """
    Агрегат Куста скважин в момент времени t
    """

    def __init__(self, geology_params: value_objects.GeologyProperties) -> None:
        """
        Инициализировать переменные
        :param geology_params: геологические параметры
        """
        self._geology_params = geology_params
        self._wells: dict[uuid.UUID, entities.Well] = {}

    def add_well(self, well: entities.Well) -> None:
        """
        Добавить скважину в куст
        :param well: объект скважины
        """

        if well.wellbore_pressure > self._geology_params.layer_pressure:
            raise ValueError("Забойное давление должно быть меньше пластового")

        if well.radius > self._geology_params.supply_contour_radius:
            raise ValueError("Радиус скважины должен быть меньше радиуса контура питания")

        if self._wells.get(well.id):
            raise ValueError("Скважина с данным идентификатором уже принадлежит кусту")

        self._wells[well.id] = well

    def calc_cluster_oil_rate(self) -> float:
        """
        Рассчитать дебит куста
        :return: дебит куста
        """

        oil_rate = 0

        for well in self._wells.values():
            oil_rate += well.calc_oil_rate(
                self._geology_params.permeability,
                self._geology_params.thickness,
                self._geology_params.layer_pressure,
                self._geology_params.supply_contour_radius,
                self._geology_params.oil_viscosity
            )

        return oil_rate
