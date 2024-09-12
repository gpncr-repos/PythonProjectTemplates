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
        :param name: имя скважины
        :param wellbore_pressure: забойное давление, МПа
        :param radius: радиус скважины, м
        """

        self.id = id_
        self.name = name
        self._wellbore_pressure = wellbore_pressure
        self._radius = radius


    @property
    def wellbore_pressure(self) -> float:
        """
        Получить забойное давление скважины
        """

        return self._wellbore_pressure

    @wellbore_pressure.setter
    def wellbore_pressure(self, value: float) -> None:
        """
        Задать забойное давление скважины
        :param value: значение давления
        """

        self._wellbore_pressure = value

    @property
    def radius(self) -> float:
        """
        Получить радиус скважины
        """

        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """
        Задать радиус скважины
        :param value: значение радиуса
        """

        self._radius = value

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
            (layer_pressure - self._wellbore_pressure) * const.ClusterDomain.mega_pascal_si_converter /
            math.log(supply_contour_radius / self._radius)
        )