import uuid
from dataclasses import dataclass

from interfaces import base_db_model


@dataclass
class Well(base_db_model.BaseDBModel):
    """
    Модель скважины
    """

    id: uuid.UUID
    name: str
    radius: float
    cluster_id: uuid.UUID
