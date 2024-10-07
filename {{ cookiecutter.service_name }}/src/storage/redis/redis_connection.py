# thirdparty
import redis
from redis import asyncio as aioredis

# project
from config.redis_config import RedisConfig


class RedisConnection:

    def __init__(self, config: RedisConfig):
        """
        Инициализация синхронного подключения к Redis.

        :param config: Конфиг Redis
        """
        self.connection = redis.from_url(config.db_dsn)

    def get_connection(self) -> redis.Redis:
        """
        Получить синхронное соединение с Redis
        :return: соединение
        """
        return self.connection

    def close_connection(self):
        """Закрыть синхронное соединение с Redis."""
        self.connection.close()


class RedisAsyncConnection:

    def __init__(self, config: RedisConfig):
        """
        Инициализация асинхронного подключения к Redis.

        :param config: Конфиг Redis
        """
        self.connection = aioredis.from_url(config.db_dsn)

    def get_connection(self) -> aioredis.Redis:
        """
        Получить асинхронное соединение с Redis
        :return: соединение
        """
        return self.connection

    async def close_connection(self):
        """Закрыть асинхронное соединение с Redis."""
        await self.connection.aclose()
