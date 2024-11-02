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
        self.redis_url = str(config.db_dsn)

    def get_connection(self) -> redis.Redis:
        """
        Получить синхронное соединение с Redis
        :return: соединение
        """
        return redis.from_url(self.redis_url)


class RedisAsyncConnection:

    def __init__(self, config: RedisConfig):
        """
        Инициализация асинхронного подключения к Redis.

        :param config: Конфиг Redis
        """
        self.redis_url = str(config.db_dsn)

    def get_connection(self) -> aioredis.Redis:
        """
        Получить асинхронное соединение с Redis
        :return: соединение
        """
        return aioredis.from_url(self.redis_url)
