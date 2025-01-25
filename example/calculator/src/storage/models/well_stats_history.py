import dataclasses
import datetime
import uuid


@dataclasses.dataclass(frozen=True)
class WellStatsHistory:
    """
    Модель истории работы скважины
    """

    id: uuid.UUID
    dt: datetime.datetime
    wellbore_pressure: float
    well_id: uuid.UUID
