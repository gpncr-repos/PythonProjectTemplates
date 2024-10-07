import dotenv
from pydantic import AmqpDsn, Field, computed_field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class RabbitMQConfig(BaseSettings):
    """
    Класс настроек для приложения
    """

    rmq_host: str = Field(description="Хост брокера", default="localhost")
    rmq_port: int = Field(description="Порт брокера", default=5672)

    rmq_user: str = Field(description="Имя пользователя", default="guest")
    rmq_password: str = Field(description="Пароль", default="guest")

    exchange: str = Field(description="Название обменника сообщениями", default="exchange")
    queue: str = Field(description="Название очереди", default="queue")
    routing_key: str = Field(description="Ключ маршрутизации", default="routing_key")

    @computed_field
    @property
    def rabbit_mq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            host=self.rmq_host,
            port=self.rmq_port,
            username=self.rmq_user,
            password=self.rmq_password,
            scheme="amqp"
        )


config = RabbitMQConfig()
