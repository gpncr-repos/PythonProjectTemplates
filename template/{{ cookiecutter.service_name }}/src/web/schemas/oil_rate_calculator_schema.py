import uuid

from pydantic import Field

from interfaces import base_web_schema
from interfaces.base_web_schema import BaseWebSchema


class WellSchema(base_web_schema.BaseWebSchema):
    """
    Схема данных модели скважины
    """

    id_: uuid.UUID = Field(description="Идентификатор скважины", alias="id")
    name: str = Field(description="Название скважины")
    wellbore_pressure: float = Field(description="Забойное давление, МПа", alias="wellborePressure")
    radius: float = Field(description="Радиус скважины, м")


class GeologyPropertiesSchema(base_web_schema.BaseWebSchema):
    """
    Схема модели данных о геологическом пласте
    """

    permeability: float = Field(description="Проницаемость пласта, мД")
    thickness: float = Field(description="Мощность пласта, м")
    layer_pressure: float = Field(description="Пластовое давление, МПа", alias="layerPressure")
    supply_contour_radius: float = Field(description="Радиус контура питания, м", alias="supplyContourRadius")
    oil_viscosity: float = Field(description="Вязкость нефти, мПа*с", alias="oilViscosity")


class ClusterSchema(base_web_schema.BaseWebSchema):
    """
    Схема данных модели куста
    """

    geology_params: GeologyPropertiesSchema = Field(description="Геологические параметры пласта", alias="geologyParams")
    wells: list[WellSchema] = Field(description="Список скважин")


class ClusterOilRate(base_web_schema.BaseWebSchema):
    oil_rate: float = Field(description="Дебит нефти для куста", alias="oilRate")