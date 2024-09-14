from pydantic import BaseModel, ConfigDict


class BaseWebSchema(BaseModel):
    """
    Базовый класс для веб-схемы данных
    """

    pass


class ConfigMixin:
    """
    Миксин конфига для DTO
    """

    model_config = ConfigDict(populate_by_name=True)
