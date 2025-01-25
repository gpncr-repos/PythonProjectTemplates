# project
from config import pg_config
from dependency_injector import containers, providers
from interfaces import base_postgres_cursor_proxy as cursor_proxy
from repositories import asyncpg_repository, psycopg_repository
from storage.raw_postgres import connection_proxy
from tools.factories import asyncpg_connection_pool_factory, psycopg_connection_pool_factory
from uows import asyncpg_uow, psycopg_uow

config = pg_config.pg_config


class PsycopgSyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через psycopg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    connection_pool_factory = providers.Singleton(
        psycopg_connection_pool_factory.PsycopgPoolFactory,
        config.postgres_dsn,
        config.connection_pool_size,
    )
    cursor_type = providers.AbstractFactory(cursor_proxy.BasePsycopgCursorProxy)
    connection_proxy = providers.Factory(
        connection_proxy.PsycopgConnectionProxy, connection_pool_factory, cursor_type
    )

    # Добавить провайдеры конкретных реализаций репозиториев
    psycopg_repository = providers.Factory(
        psycopg_repository.PsycopgSyncRepository, connection_proxy
    )

    # Добавить провайдеры конкретных реализаций UOW
    psycopg_uow = providers.Factory(psycopg_uow.PsycopgSyncUOW, psycopg_repository)


class AsyncpgContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через asyncpg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

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
    asyncpg_repository = providers.Factory(asyncpg_repository.AsyncpgRepository, connection_proxy)

    # Добавить провайдеры конкретных реализаций UOW
    asyncpg_uow = providers.Factory(asyncpg_uow.AsyncpgUOW, asyncpg_repository)
