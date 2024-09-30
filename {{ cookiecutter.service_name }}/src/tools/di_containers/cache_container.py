# thirdparty
from dependency_injector import containers, providers

# project
from storage.redis import redis_connection
from repositories import redis_repository


class RedisCacheContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с кэшем в бд Redis
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    redis_sync_conn = providers.Factory(redis_connection.RedisConnection)
    redis_async_conn = providers.Factory(redis_connection.RedisAsyncConnection)

    redis_sync_repository = providers.Factory(
        redis_repository.SyncRedisRepository, redis_sync_conn
    )
    redis_async_repository = providers.Factory(
        redis_repository.AsyncRedisRepository, redis_async_conn
    )
