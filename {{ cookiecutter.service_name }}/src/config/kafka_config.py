import dotenv
from pydantic import Field, computed_field
from pydantic.v1 import KafkaDsn
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class KafkaConfig(BaseSettings):
    """
    Класс настроек для Kafka
    """

    host: str = Field(description="Хост Kafka", default="localhost", alias="KAFKA_HOST")
    port: str = Field(description="Порт Kafka", default="29092", alias="KAFKA_PORT")
    scheme: str = Field(description="Протокол", default="kafka", alias="KAFKA_SCHEME")

    # Добавить название топика как поле класса
    topic: str = Field(description="Название топика", default="")

    # Добавить название группы как поле класса
    group: str = Field(description="Название группы консюмеров", default="")

    @computed_field
    @property
    def kafka_dsn(self) -> str:
        return KafkaDsn.build(host=self.host, port=self.port, scheme=self.scheme)


config = KafkaConfig()
