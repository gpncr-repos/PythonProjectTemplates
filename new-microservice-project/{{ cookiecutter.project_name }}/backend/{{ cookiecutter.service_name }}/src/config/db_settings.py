from typing import Optional

import dotenv
from pydantic_core.core_schema import ValidationInfo
from pydantic import PostgresDsn, field_validator, RedisDsn, Field

from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class DBSettings(BaseSettings):
    user: str = Field(alias="PG_USER")
    password: str = Field(alias="PG_PASSWORD")
    host: str = Field(alias="PG_HOST")
    port: int = Field(alias="PG_PORT", default=5432)
    db_name: str = Field(alias="PG_DB_NAME")

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


class RedisSettings(BaseSettings):
    user: str = Field(alias="REDIS_USER")
    password: str = Field(alias="REDIS_PASSWORD")
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT", default=6379)
    db_id: str = Field(alias="REDIS_DB")

    redis_dns: Optional[RedisDsn | str] = None

    @field_validator("redis_dns")  # noqa
    @classmethod
    def create_connection(cls, v: str, values: ValidationInfo) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=values.data.get("user"),
            host=values.data.get("host"),
            port=values.data.get("port"),
            password=values.data.get("password"),
            path=values.data.get('db_id')
        )
