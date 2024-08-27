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
        self.dns = settings.redis.dns

    def __call__(self) -> Redis:
        """
        Получить объект подключения Redis
        :return: Объект подключения Redis
        """
        return from_url(self.dns)


class RedisAsyncConnection:
    """
    Класс подключения к redis
    """

    def __init__(self, settings: Settings) -> None:
        """
        Инициализировать переменные
        """
        self.dns = settings.redis.dns

    async def __call__(self) -> aioredis.Redis:
        """
        Получить объект подключения Redis
        :return: Объект подключения Redis
        """
        return await aioredis.from_url(self.dns)
