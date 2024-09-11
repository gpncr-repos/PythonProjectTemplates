from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Класс настроек для приложения
    """

    project_name: str = Field(description="Название проекта", default="{{ cookiecutter.project_name }}")
    app_name: str = Field(description="Название сервиса", default="{{ cookiecutter.service_name }}")
    app_version: str = Field(description="Версия сервиса", default="{{ cookiecutter.service_version }}")

    app_host: str = Field(description="Хост сервиса", default="{{ cookiecutter.service_host }}", alias="PROJECT_HOST")
    app_port: int = Field(description="Порт сервиса", default="{{ cookiecutter.service_port }}", alias="PROJECT_PORT")

    okd_stage: str = Field(description="Состояние OKD", default="{{ cookiecutter.okd_stage }}")


app_config = Config()
