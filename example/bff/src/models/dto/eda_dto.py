import datetime
import uuid

from pydantic import Field

from interfaces import base_dto
from tools import enums


class EDATypeDTO(base_dto.BaseDTO):
    """
    DTO, содержащий информацию о типе события и его свойства
    """

    event_type: enums.CommandType = Field(description="Тип события EDA")
    cluster_id: uuid.UUID = Field(description="Идентификатор куста")
    message: str = Field(description="Описание события")
    calc_date: datetime.datetime = Field(description="Дата замеров для расчета")
