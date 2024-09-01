# stdlib
import dotenv

#thirdparty
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class RedisSettings(BaseSettings):
    user: str = Field(alias="REDIS_USER")
    password: str = Field(alias="REDIS_PASSWORD")
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")
    db_id: str = Field(alias="REDIS_DB")

    @property
    def dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.user,
            host=self.host,
            port=self.port,
            password=self.password,
            path=self.db_id,
        )
