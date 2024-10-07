# stdlib
import dotenv

#thirdparty
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class RedisConfig(BaseSettings):
    """
    Класс настроек для Redis
    """

    user: str = Field(alias="REDIS_USER", description="Имя пользователя Redis")
    password: str = Field(alias="REDIS_PASSWORD", description="Пароль пользователя Redis")
    host: str = Field(alias="REDIS_HOST", description="Хост подключения к Redis")
    port: int = Field(6379, alias="REDIS_PORT", description="Порт подключения к Redis")
    db_id: str = Field(alias="REDIS_DB", description="Идентификатор БД Redis")
    broker_id: str = Field(alias="REDIS_BROKER", description="Идентификатор брокера Redis")

    @property
    def db_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.user,
            host=self.host,
            port=self.port,
            password=self.password,
            path=self.db_id,
        )

    @property
    def broker_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.user,
            host=self.host,
            port=self.port,
            password=self.password,
            path=self.broker_id,
        )
