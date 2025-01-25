import uuid
from dataclasses import dataclass

from interfaces import base_db_model


@dataclass
class Cluster(base_db_model.BaseDBModel):
    """
    Модель куста
    """

    id: uuid.UUID
    name: str
    geology_params_id: uuid.UUID
