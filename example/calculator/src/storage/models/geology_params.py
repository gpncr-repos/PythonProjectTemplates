import dataclasses
import datetime
import uuid


@dataclasses.dataclass(frozen=True)
class GeologyProperties:
    """
    Модель геологических параметров
    """

    id: uuid.UUID
    dt: datetime.datetime
    permeability: float
    thickness: float
    layer_pressure: float
    supply_contour_radius: float
    oil_viscosity: float
