import dataclasses

from interfaces import base_domain_model as domain


@dataclasses.dataclass(frozen=True)
class GeologyProperties(domain.DomainValueObject):
    """
    Класс, описывающий геологические параметры пласта
    :param permeability: проницаемость пласта, мД
    :param thickness: мощность пласта, м
    :param layer_pressure: пластовое давление, МПа
    :param supply_contour_radius: радиус контура питания, м
    :param oil_viscosity: вязкость нефти, мПа*с
    """

    permeability: float
    thickness: float
    layer_pressure: float
    supply_contour_radius: float
    oil_viscosity: float
