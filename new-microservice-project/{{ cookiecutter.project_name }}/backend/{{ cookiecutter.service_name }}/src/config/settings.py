from .db_settings import DBSettings, RedisSettings


class Settings:
    product_name: str = "{{cookiecutter.project_name}}"
    service_name: str = "{{cookiecutter.service_name}}"
    service_version: str = "0.0.0.0"

    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
