# thirdparty
import dotenv
from pydantic import Field, PostgresDsn
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
    connection_pool_size: int = Field(default=10, description="Размер пула соединений")
    server_side_cursor_name: str = Field(
        default="test_cursor", description="Название server-side курсора"
    )

    @property
    def psycopg_dsn(self) -> PostgresDsn:
        """
        Получение url для синхронного подключения к Postgres через psycopg
        :return: url
        """

        return self._build_dsn(
            scheme="postgresql",
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


pg_config = PostgresConfig()
