from pydantic import BaseModel, ConfigDict


class PydanticModel(BaseModel):
    """
    Базовый класс модели Pydantic
    """

    model_config = ConfigDict(populate_by_name=True)
