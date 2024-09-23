import dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class KafkaConfig(BaseSettings):
    """
    Класс настроек для брокера сообщений
    """

    host: str = Field("localhost:29092", alias="KAFKA_URL")
    topic: str = Field("")
    group: str = Field("")
    topics: list[str] = Field(default_factory=list)
    consume_topics: list[str] = Field(default_factory=list)
    kafka_consumers_enabled: bool = Field(True, alias="KAFKA_CONSUMERS_ENABLED")
    kafka_producers_enabled: bool = Field(True, alias="KAFKA_PRODUCERS_ENABLED")
