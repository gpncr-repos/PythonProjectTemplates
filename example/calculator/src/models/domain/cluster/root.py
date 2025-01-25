import uuid

from interfaces import base_domain_model as domain
from models.domain.cluster import entities, value_objects


class Cluster(domain.DomainAggregate):
    """
    Агрегат Куста скважин в момент времени t
    """

    def __init__(
        self,
        id_: uuid.UUID,
        name: str,
        geology_params: value_objects.GeologyProperties
    ) -> None:
        """
        Инициализировать переменные
        :param id_: идентификатор куста
        :param name: название куста
        :param geology_params: геологические параметры
        """

        self.id = id_
        self.name = name
        self.geology_params = geology_params
        self._wells: dict[uuid.UUID, entities.Well] = {}

    def add_well(self, well: entities.Well) -> None:
        """
        Добавить скважину в куст
        :param well: объект скважины
        """

        if self._wells.get(well.id):
            raise ValueError("Скважина с данным идентификатором уже принадлежит кусту")

        if well.wellbore_pressure > self.geology_params.layer_pressure:
            raise ValueError("Забойное давление должно быть меньше пластового")

        if well.radius > self.geology_params.supply_contour_radius:
            raise ValueError("Радиус скважины должен быть меньше радиуса контура питания")

        self._wells[well.id] = well

    def calc_cluster_oil_rate(self) -> float:
        """
        Рассчитать дебит куста
        :return: дебит куста
        """

        oil_rate = 0

        for well in self._wells.values():
            oil_rate += well.calc_oil_rate(
                self.geology_params.permeability,
                self.geology_params.thickness,
                self.geology_params.layer_pressure,
                self.geology_params.supply_contour_radius,
                self.geology_params.oil_viscosity
            )

        return oil_rate
