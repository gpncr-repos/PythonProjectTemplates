from config.postgres_settings import PostgresSettings
from config.kafka_settings import KafkaSettings
from config.redis_settings import RedisSettings


class Settings:
    product_name: str = "{{cookiecutter.project_name}}"
    service_name: str = "{{cookiecutter.service_name}}"
    service_version: str = "0.0.0.0"
    okd_stage: str = "DEV"
    app_host: str = "localhost"
    app_port: int = 8000

    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()