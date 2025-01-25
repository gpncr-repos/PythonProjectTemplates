from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Класс настроек для приложения
    """

    project_name: str = Field(
        description="Название проекта", default="oil_rate_calculator"
    )
    app_name: str = Field(
        description="Название сервиса", default="calculator"
    )
    app_version: str = Field(
        description="Версия API", default="v1"
    )

    app_host: str = Field(
        description="Хост сервиса",
        default="0.0.0.0",
        alias="PROJECT_HOST",
    )
    app_port: int = Field(
        description="Порт сервиса",
        default="8081",
        alias="PROJECT_PORT",
    )

    okd_stage: str = Field(
        description="Состояние OKD", default="DEV"
    )


app_config = Config()
