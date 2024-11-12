# thirdparty
import psycopg_pool

# project
from config import pg_config
from dependency_injector import containers, providers
from interfaces import base_postgres_cursor_proxy as cursor_proxy
from repositories import raw_postgres_repository
from repositories.tools import sql_tools
from storage.psycopg import psycopg_proxy
from uows import psycopg_uow

config = pg_config.pg_config


class PsycopgSyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через psycopg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    dsn = providers.Factory(str, pg_config.pg_config.psycopg_dsn)
    connection_pool = providers.Singleton(
        psycopg_pool.ConnectionPool, dsn, max_size=config.connection_pool_size
    )
    cursor_type = providers.AbstractFactory(cursor_proxy.BasePsycopgCursorProxy)
    connection_proxy = providers.Factory(
        psycopg_proxy.PsycopgConnectionProxy, connection_pool, cursor_type
    )
    sql_creator = providers.Factory(sql_tools.PsycopgRawSQLCreator)
    psycopg_repository = providers.Factory(
        raw_postgres_repository.PsycopgSyncRepository, connection_proxy, sql_creator
    )
    psycopg_uow = providers.Factory(psycopg_uow.PsycopgSyncUOW, psycopg_repository)
