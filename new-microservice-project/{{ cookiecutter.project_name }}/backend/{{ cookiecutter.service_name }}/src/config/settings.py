from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env',)
    )

    product_name: str = "{{cookiecutter.project_name}}"
    service_name: str = "{{cookiecutter.service_name}}"
    service_version: str = "0.0.0.0"


settings = Settings
