# thirdparty
from redis import asyncio as aioredis, from_url, Redis

# project
from config.settings import Settings


class RedisConnection:
    """
    Класс подключения к redis
    """

    def __init__(self, settings: Settings) -> None:
        """
        Инициализировать переменные
        """
        self.dsn = settings.redis.dsn

    def __call__(self) -> Redis:
        """
        Получить объект подключения Redis
        :return: Объект подключения Redis
        """
        return from_url(self.dsn)


class RedisAsyncConnection:
    """
    Класс подключения к redis
    """

    def __init__(self, settings: Settings) -> None:
        """
        Инициализировать переменные
        """
        self.dsn = settings.redis.dsn

    async def __call__(self) -> aioredis.Redis:
        """
        Получить объект подключения Redis
        :return: Объект подключения Redis
        """
        return await aioredis.from_url(self.dsn)
