from cookiecutter.main import cookiecutter
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Класс настроек для приложения
    """

    project_name: str = Field(description="Название проекта", default="{{ cookiecutter.project_name }}")
    app_name: str = Field(description="Название сервиса", default="{{ cookiecutter.service_name }}")
    app_version: str = Field(description="Версия API", default="{{ cookiecutter.api_version }}")

    app_host: str = Field(description="Хост сервиса", default="{{ cookiecutter.service_host }}", alias="PROJECT_HOST")
    app_port: int = Field(description="Порт сервиса", default="{{ cookiecutter.service_port }}", alias="PROJECT_PORT")

    okd_stage: str = Field(description="Состояние OKD", default="{{ cookiecutter.okd_stage }}")
    {% if cookiecutter.api_architecture == "grpc" %}
    grpc_host: str = Field(description="Хост grpc-сервера", default="localhost")
    grpc_port: int = Field(description="Порт grpc-сервера", default=50051)
    grpc_workers_count: int = Field(description="Количество воркеров для grpc-сервера", default=10)

    def get_grpc_address(self) -> str:
        """
        Получить адрес grpc-сервера
        :return: адрес сервера grpc
        """

        return f"{self.grpc_host}:{self.grpc_port}"
    {% endif %}


app_config = Config()
