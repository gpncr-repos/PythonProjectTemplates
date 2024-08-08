from typing import Optional

from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', )
    )

    user: str = ''
    password: str = ''
    host: str = ''
    port: int = 5432
    db_name: str = ''

    pg_sync_dsn: Optional[PostgresDsn | str] = None
    pg_async_dsn: Optional[PostgresDsn | str] = None

    @field_validator('pg_sync_dsn')  # noqa
    @classmethod
    def create_sync_connection(cls, v: str, values: ValidationInfo) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.data.get("user"),
            password=values.data.get("password"),
            host=values.data.get("host"),
            port=values.data.get("port"),
            path=values.data.get("db_name")
        )

    @field_validator('pg_async_dsn')  # noqa
    @classmethod
    def create_async_connection(cls, v: str, values: ValidationInfo) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("user"),
            password=values.data.get("password"),
            host=values.data.get("host"),
            port=values.data.get("port"),
            path=values.data.get("db_name")
        )
