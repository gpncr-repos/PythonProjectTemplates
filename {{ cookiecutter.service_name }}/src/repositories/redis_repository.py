# thirdparty
import redis

# project
from storage.redis import redis_connection
from interfaces.base_repository import BaseRepository


class SyncRedisRepository(BaseRepository):
    """
    Репозиторий для синхронной работы с кэшем
    """
    def __init__(self, connection: redis_connection.RedisConnection):
        """
        Инициализировать переменные
        :param connection: соедидинение c кэш БД
        """
        self.connection = connection.get_connection()

    def create(self, key, value, ttl: int = None) -> None:
        """
        Создать запись в бд
        :param key: имя записи
        :param value: значение записи
        :param ttl: время жизни записи
        """
        try:
            if ttl:
                self.connection.set(key, value, ex=ttl)
            else:
                self.connection.set(key, value)
        except redis.RedisError as e:
            raise e

    def retrieve(self, key) -> any:
        """
        Получить запись из бд по ключу
        :param key: имя записи
        """
        try:
            value = self.connection.get(key)
        except redis.RedisError as e:
            raise e
        return value

    def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    def update(self, key, new_value) -> None:
        """
        Обновить запись в бд
        :param key: имя записи
        :param new_value: новое значение для записи
        """
        try:
            self.connection.set(key, new_value)
        except redis.RedisError as e:
            raise e

    def delete(self, key) -> None:
        """
        Удалить запись из бд
        :param key: имя записи
        """
        try:
            self.connection.delete(key)
        except redis.RedisError as e:
            raise e


class AsyncRedisRepository(BaseRepository):
    """
    Репозиторий для асинхронной работы с кэшем
    """
    def __init__(self, connection: redis_connection.RedisAsyncConnection):
        """
        Инициализировать переменные
        :param connection: асинхронное соедидинение c кэш БД
        """
        self.connection = connection.get_connection()

    async def create(self, key, value, ttl: int = None) -> None:
        """
        Создать запись в бд
        :param key: имя записи
        :param value: значение записи
        :param ttl: время жизни записи
        """
        try:
            if ttl:
                await self.connection.set(key, value, ex=ttl)
            else:
                await self.connection.set(key, value)
        except redis.RedisError as e:
            raise e

    async def retrieve(self, key) -> any:
        """
        Получить запись из бд по ключу
        :param key: имя записи
        """
        try:
            value = await self.connection.get(key)
        except redis.RedisError as e:
            raise e
        return value

    async def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    async def update(self, key, new_value) -> None:
        """
        Обновить запись в бд
        :param key: имя записи
        :param new_value: новое значение для записи
        """
        try:
            await self.connection.set(key, new_value)
        except redis.RedisError as e:
            raise e

    async def delete(self, key) -> None:
        """
        Удалить запись из бд
        :param key: имя записи
        """
        try:
            await self.connection.delete(key)
        except redis.RedisError as e:
            raise e
