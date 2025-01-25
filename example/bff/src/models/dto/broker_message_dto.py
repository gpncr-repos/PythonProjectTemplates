import datetime
import uuid

from pydantic import Field

from interfaces import base_dto


class BrokerMessageDTO(base_dto.BaseDTO):
    """
    DTO, содержащий сообщение для брокера
    """

    id: uuid.UUID = Field(
        description="Идентификатор сообщения", default_factory=lambda: uuid.uuid4()
    )
    body: dict = Field(description="Тело сообщения")
    date: datetime.datetime = Field(
        description="Дата создания сообщения",
        default_factory=lambda: datetime.datetime.now(),
    )
