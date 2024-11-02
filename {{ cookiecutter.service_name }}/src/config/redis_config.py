# stdlib
import dotenv

# thirdparty
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class RedisConfig(BaseSettings):
    """
    Класс настроек для Redis
    """

    host: str = Field(alias="REDIS_HOST", description="Хост подключения к Redis")
    port: int = Field(6379, alias="REDIS_PORT", description="Порт подключения к Redis")
    password: str = Field(alias="REDIS_PASSWORD", description="Пароль Redis")
    db_id: str = Field(alias="REDIS_DB", description="Идентификатор БД Redis")
    broker_id: str = Field(
        alias="REDIS_BROKER", description="Идентификатор брокера Redis"
    )

    def _build_dsn(self, path: str):
        return RedisDsn.build(
            scheme="redis",
            host=self.host,
            port=self.port,
            password=self.password,
            path=path,
        )

    @property
    def db_dsn(self) -> RedisDsn:
        return self._build_dsn(self.db_id)

    @property
    def broker_dsn(self) -> RedisDsn:
        return self._build_dsn(self.broker_id)

redis_config = RedisConfig()
