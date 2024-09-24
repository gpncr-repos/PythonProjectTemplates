# thirdparty
from dependency_injector import containers, providers

# project
from cache import redis_connection
from repositories import cache_repository


class RedisCacheContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с кэшем в бд Redis
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    redis_sync_conn = providers.Factory(redis_connection.RedisConnection)
    redis_async_conn = providers.Factory(redis_connection.RedisAsyncConnection)

    cache_sync_repository = providers.Factory(
        cache_repository.SyncRedisRepository, redis_sync_conn
    )
    cache_async_repository = providers.Factory(
        cache_repository.AsyncRedisRepository, redis_async_conn
    )
