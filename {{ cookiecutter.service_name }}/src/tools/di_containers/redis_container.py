# thirdparty
from dependency_injector import containers, providers

# project
from config.redis_config import redis_config
from storage.redis import redis_connection
from repositories import redis_repository
from uows import redis_uow


class RedisSyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с синхронными провайдерами для работы с кэшем в бд Redis
    """

    wiring_config = containers.WiringConfiguration(modules=None)

    redis_sync_conn = providers.Factory(redis_connection.RedisConnection, redis_config)
    redis_sync_repository = providers.Factory(redis_repository.SyncRedisRepository, redis_sync_conn)
    redis_sync_uow = providers.Factory(redis_uow.SyncRedisUOW, redis_sync_repository)


class RedisAsyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с асинхронными провайдерами для работы с кэшем в бд Redis
    """

    wiring_config = containers.WiringConfiguration(modules=None)

    redis_async_conn = providers.Factory(redis_connection.RedisAsyncConnection, redis_config)
    redis_async_repository = providers.Factory(redis_repository.AsyncRedisRepository, redis_async_conn)
    redis_async_uow = providers.Factory(redis_uow.AsyncRedisUOW, redis_async_repository)
