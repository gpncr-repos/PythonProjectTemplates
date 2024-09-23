# thirdparty
from redis import asyncio as aioredis

# project
from config.redis_config import RedisConfig


class RedisConnection:
    def __init__(self, config: RedisConfig):
        """
        Инициализация асинхронного подключения к Redis.

        :param redis_dsn:
        """
        self.dsn = config.dsn
        self.connection = None

    async def connect(self):
        """Устанавливает асинхронное соединение с Redis."""
        try:
            self.connection = await aioredis.from_url(self.dsn)
        except Exception as e:
            raise e

    async def set(self, key, value):
        """Сохраняет значение по ключу в Redis."""
        if self.connection:
            try:
                await self.connection.set(key, value)
            except Exception as e:
                raise e
        else:
            raise ConnectionError("Соединение с Redis не установлено.")

    async def get(self, key):
        """Получает значение по ключу из Redis."""
        if self.connection:
            try:
                value = await self.connection.get(key)
                return value
            except Exception as e:
                raise e
        else:
            raise ConnectionError("Соединение с Redis не установлено.")

    async def close(self):
        """Закрывает асинхронное соединение с Redis."""
        if self.connection:
            await self.connection.close()
            self.connection = None
