import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Класс настроек для генерации шаблона
    """

    template_src_path: pathlib.Path = Field(
        description="Путь к папке src шаблона",
        default=pathlib.Path.cwd().resolve().parent / "{{ cookiecutter.service_name }}" / "src"
    )


template_config = Config()
