import uuid

from pydantic import Field

from interfaces import base_dto


class GeologyPropertiesDTO(base_dto.BaseDTO, base_dto.ConfigMixin):
    """
    DTO, содержащий данные о геологическом пласте
    """

    permeability: float = Field(description="Проницаемость пласта, мД")
    thickness: float = Field(description="Мощность пласта, м")
    layer_pressure: float = Field(description="Пластовое давление, МПа")
    supply_contour_radius: float = Field(description="Радиус контура питания, м")
    oil_viscosity: float = Field(description="Вязкость нефти, мПа*с")


class WellPropertiesDTO(base_dto.BaseDTO, base_dto.ConfigMixin):
    """
    DTO, содержащий данные о скважине
    """

    id_: uuid.UUID = Field(description="Идентификатор скважины")
    name: str = Field(description="Название скважины")
    wellbore_pressure: float = Field(description="Забойное давление, МПа")
    radius: float = Field(description="Радиус скважины, м")
