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
        self.dsn = config.dsn
        self.connection = None

    def get_connection(self) -> redis.Redis:
        """
        Получить синхронное соединение с Redis
        :return: соединение
        """
        if not self.connection:
            try:
                self.connection = redis.from_url(self.dsn)
            except redis.ConnectionError as e:
                raise e
        return self.connection

    def close_connection(self):
        """Закрыть синхронное соединение с Redis."""
        if self.connection:
            self.connection.close()
            self.connection = None


class RedisAsyncConnection:

    def __init__(self, config: RedisConfig):
        """
        Инициализация асинхронного подключения к Redis.

        :param config: Конфиг Redis
        """
        self.dsn = config.dsn
        self.connection = None

    def get_connection(self) -> aioredis.Redis:
        """
        Получить асинхронное соединение с Redis
        :return: соединение
        """
        if not self.connection:
            try:
                self.connection = aioredis.from_url(self.dsn)
            except Exception as e:
                raise e
        return self.connection

    async def close_connection(self):
        """Закрыть асинхронное соединение с Redis."""
        if self.connection:
            await self.connection.close()
            self.connection = None
