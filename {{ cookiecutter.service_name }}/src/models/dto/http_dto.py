from pydantic import Field

from interfaces import base_dto


class HTTPRequestDTO(base_dto.BaseDTO):
    """
    DTO, содержащий информацию для HTTP-запроса
    """

    url: str = Field(description="URL запроса")
    headers: dict | None = Field(description="Заголовки", default=None)
    query_params: dict | None = Field(description="Параметры запроса", default=None)
    payload: dict | None = Field(description="Body запроса", default=None)


class HTTPResponseDTO(base_dto.BaseDTO):
    """
    DTO, содержащий информацию ответа HTTP-запроса
    """

    status: int = Field(description="Статус ответа")
    payload: dict | list[dict] | None = Field(description="Body ответа", default=None)
