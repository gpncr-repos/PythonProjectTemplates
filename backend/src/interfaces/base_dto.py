from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Базовый класс DTO
    """

    pass


class ConfigMixin:
    """
    Миксин конфига для DTO
    """

    model_config = ConfigDict(populate_by_name=True)
