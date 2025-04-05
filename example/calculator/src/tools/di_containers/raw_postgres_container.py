# project
from config import pg_config
from dependency_injector import containers, providers
from interfaces import base_postgres_cursor_proxy as cursor_proxy
from repositories import cluster_repository
from storage.raw_postgres import connection_proxy
from tools.factories import asyncpg_connection_pool_factory
from uows import asyncpg_uow

config = pg_config.pg_config


class AsyncpgContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через asyncpg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(packages=["services"])

    connection_pool_factory = providers.Singleton(
        asyncpg_connection_pool_factory.AsyncpgPoolFactory,
        config.postgres_dsn,
        config.connection_pool_size,
    )
    cursor_type = providers.AbstractFactory(cursor_proxy.BaseAsyncpgCursorProxy)
    connection_proxy = providers.Factory(
        connection_proxy.AsyncpgConnectionProxy, connection_pool_factory, cursor_type
    )

    # Добавить провайдеры конкретных реализаций репозиториев
    cluster_repository = providers.Factory(cluster_repository.ClusterRepository, connection_proxy)

    # Добавить провайдеры конкретных реализаций UOW
    asyncpg_uow = providers.Factory(asyncpg_uow.AsyncpgUOW, cluster_repository)
