# stdlib
from typing import Callable

# thirdparty
import redis

# project
from storage.redis import redis_connection
from interfaces.base_repository import BaseRepository


class RedisErrorCatcherDecorator:
    """
    Класс, реализующий метод-декоратор для отлавливания ошибок в репозитории Redis
    """

    def _catch_sync_exception(method: Callable) -> Callable:
        """
        Отловить ошибку при синхронном запросе к бд Redis
        :param method: метод репозитория
        :return: функция-обертка
        """

        def execute_method(self, *args, **kwargs) -> any:
            """
            Выполнить метод репозитория
            """

            try:
                return method(self, *args, **kwargs)
            except redis.RedisError as redis_error:
                raise redis_error
            except NotImplementedError as not_impl_error:
                raise not_impl_error

        return execute_method

    def _catch_async_exception(method: Callable) -> Callable:
        """
        Отловить ошибку при асинхронном запросе к бд Redis
        :param method: метод репозитория
        :return: функция-обертка
        """

        async def execute_method(self, *args, **kwargs) -> any:
            """
            Выполнить метод репозитория
            """

            try:
                return await method(self, *args, **kwargs)
            except redis.RedisError as redis_error:
                raise redis_error
            except NotImplementedError as not_impl_error:
                raise not_impl_error

        return execute_method

    catch_sync_exception = staticmethod(_catch_sync_exception)
    catch_async_exception = staticmethod(_catch_async_exception)


class SyncRedisRepository(BaseRepository):
    """
    Репозиторий для синхронной работы с кэшем
    """

    def __init__(self, connection: redis_connection.RedisConnection):
        """
        Инициализировать переменные
        :param connection: синхронное соедидинение Redis
        """
        self.connection = connection.get_connection()

    @RedisErrorCatcherDecorator.catch_sync_exception
    def create(self, key, value, ttl: int | None = None) -> None:
        """
        Создать запись в бд
        :param key: имя записи
        :param value: значение записи
        :param ttl: время жизни записи
        """

        if ttl:
            self.connection.set(key, value, ex=ttl)
        else:
            self.connection.set(key, value)

    @RedisErrorCatcherDecorator.catch_sync_exception
    def retrieve(self, key) -> any:
        """
        Получить запись из бд по ключу
        :param key: имя записи
        """
        value = self.connection.get(key)
        return value

    @RedisErrorCatcherDecorator.catch_sync_exception
    def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    @RedisErrorCatcherDecorator.catch_sync_exception
    def update(self, key, new_value) -> None:
        """
        Обновить запись в бд
        :param key: имя записи
        :param new_value: новое значение для записи
        """
        self.connection.set(key, new_value)

    @RedisErrorCatcherDecorator.catch_sync_exception
    def delete(self, key) -> None:
        """
        Удалить запись из бд
        :param key: имя записи
        """
        self.connection.delete(key)


class AsyncRedisRepository(BaseRepository):
    """
    Репозиторий для асинхронной работы с кэшем
    """

    def __init__(self, connection: redis_connection.RedisAsyncConnection):
        """
        Инициализировать переменные
        :param connection: асинхронное соедидинение Redis
        """
        self.connection = connection.get_connection()

    @RedisErrorCatcherDecorator.catch_async_exception
    async def create(self, key, value, ttl: int | None = None) -> None:
        """
        Создать запись в бд
        :param key: имя записи
        :param value: значение записи
        :param ttl: время жизни записи
        """
        if ttl:
            await self.connection.set(key, value, ex=ttl)
        else:
            await self.connection.set(key, value)

    @RedisErrorCatcherDecorator.catch_async_exception
    async def retrieve(self, key) -> any:
        """
        Получить запись из бд по ключу
        :param key: имя записи
        """
        value = await self.connection.get(key)
        return value

    @RedisErrorCatcherDecorator.catch_async_exception
    async def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    @RedisErrorCatcherDecorator.catch_async_exception
    async def update(self, key, new_value) -> None:
        """
        Обновить запись в бд
        :param key: имя записи
        :param new_value: новое значение для записи
        """
        await self.connection.set(key, new_value)

    @RedisErrorCatcherDecorator.catch_async_exception
    async def delete(self, key) -> None:
        """
        Удалить запись из бд
        :param key: имя записи
        """
        await self.connection.delete(key)
