from redis.asyncio import Redis

from config.settings import Settings


class RedisConnection:
    """
    Класс подключения к redis
    """

    def __init__(self, settings: Settings) -> None:
        """
        Инициализировать переменные
        """
        self.dns = settings.redis.dns

    async def __call__(self) -> Redis:
        """
        Получить объект подключения Redis
        :return: Объект подключения Redis
        """
        ...
