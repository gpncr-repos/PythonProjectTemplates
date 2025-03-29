import uuid

# thirdparty
import dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class PostgresConfig(BaseSettings):
    """
    Класс настроек для БД
    """

    user: str = Field(alias="POSTGRES_USER", description="Имя пользователя БД", default="admin")
    password: str = Field(
        alias="POSTGRES_PASSWORD", description="Пароль пользователя БД", default="admin"
    )
    host: str = Field(
        alias="POSTGRES_HOST", description="Хост подключения к БД", default="localhost"
    )
    port: int = Field(alias="POSTGRES_PORT", default=5432, description="Порт подключения к БД")
    db_name: str = Field(alias="POSTGRES_DB", description="Имя БД", default="test")
    connection_pool_size: int = Field(alias="POOL_SIZE", description="Размер пула соединений")

    @property
    def cursor_name_salt(self) -> str:
        """
        Сгенерировать соль для названия server-side курсора
        """

        return str(uuid.uuid4())

    @property
    def postgres_dsn(self) -> PostgresDsn:
        """
        Получение url для подключения к Postgres синхронно
        :return: dsn
        """

        return PostgresDsn.build(
            scheme="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )

    @property
    def postgres_async_dsn(self) -> PostgresDsn:
        """
        Получение url для подключения к Postgres асинхронно
        :return: dsn
        """

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )


pg_config = PostgresConfig()
