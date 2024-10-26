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

    # Добавить название обменника как поле класса
    exchange: str = Field(description="Название обменника сообщениями", default="exchange")

    # Добавить название очереди как поле класса
    queue: str = Field(description="Название очереди", default="queue")

    # Добавить название ключа маршрутизации как поле класса
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
