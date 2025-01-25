import math
import uuid

from interfaces import base_domain_model as domain
from tools import const


class Well(domain.DomainEntityObject):
    """
    Сущность Скважины
    """

    def __init__(self, id_: uuid.UUID, name: str, wellbore_pressure: float, radius: float) -> None:
        """
        Инициализировать переменные
        :param id_: идентификатор скважины
        :param name: название скважины
        :param wellbore_pressure: забойное давление, МПа
        :param radius: радиус скважины, м
        """

        self.id = id_
        self.name = name
        self.wellbore_pressure = wellbore_pressure
        self.radius = radius

    def calc_oil_rate(
        self,
        permeability: float,
        thickness: float,
        layer_pressure: float,
        supply_contour_radius: float,
        oil_viscosity: float
    ) -> float:
        """
        Рассчитать дебит нефти по формуле Дюпюи
        Результат в м^3 / с
        :param permeability: проницаемость пласта
        :param thickness: мощность пласта
        :param layer_pressure: пластовое давление
        :param supply_contour_radius: радиус контура питания
        :param oil_viscosity: вязкость нефти
        :return: дебит нефти
        """

        return (
                2 * math.pi * permeability * const.ClusterDomain.milli_darcy_si_converter_coef * thickness /
                (oil_viscosity * const.ClusterDomain.milli_pascal_si_converter) *
                (layer_pressure - self.wellbore_pressure) * const.ClusterDomain.mega_pascal_si_converter /
                math.log(supply_contour_radius / self.radius)
        )
