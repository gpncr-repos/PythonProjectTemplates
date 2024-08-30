# thirdparty
import dotenv
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class PostgresSettings(BaseSettings):
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT", default=5432)
    db_name: str = Field(alias="POSTGRES_DB")


    @property
    def pg_sync_dsn(self) -> PostgresDsn:
        return self._build_dsn(
            scheme="postgresql+psycopg2",
        )

    @property
    def pg_async_dsn(self) -> PostgresDsn:
        return self._build_dsn(
            scheme="postgresql+asyncpg",
        )

    def _build_dsn(self, scheme: str) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=scheme,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )
