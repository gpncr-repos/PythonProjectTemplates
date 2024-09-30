# thirdparty
import dotenv
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class PostgresConfig(BaseSettings):
    """
    Класс настроек для БД
    """
    user: str = Field(alias="POSTGRES_USER", description="Имя пользователя БД")
    password: str = Field(alias="POSTGRES_PASSWORD", description="Пароль пользователя БД")
    host: str = Field(alias="POSTGRES_HOST", description="Хост подключения к БД")
    port: int = Field(alias="POSTGRES_PORT", default=5432, description="Порт подключения к БД")
    db_name: str = Field(alias="POSTGRES_DB", description="Имя БД")

    @property
    def pg_sync_dsn(self) -> PostgresDsn:
        """
        Получение url для синхронного подключения к Postgres
        :return: url
        """
        return self._build_dsn(
            scheme="postgresql+psycopg2",
        )

    @property
    def pg_async_dsn(self) -> PostgresDsn:
        """
        Получение url для асинхронного подключения к Postgres
        :return: url
        """
        return self._build_dsn(
            scheme="postgresql+asyncpg",
        )

    def _build_dsn(self, scheme: str) -> PostgresDsn:
        """
        Сборщик url
        :parm scheme: схема для синхронной или асинхронной работы
        :return: url
        """
        return PostgresDsn.build(
            scheme=scheme,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )
