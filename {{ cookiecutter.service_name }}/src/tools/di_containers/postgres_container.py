# thirdparty
# project
from config.pg_config import pg_config
from dependency_injector import containers, providers
from repositories import psycopg_repository
from repositories.sql_tools import PsycopgRawSQLCreator
from storage.psycopg import psycopg_proxy
from uows import psycopg_uow


class PsycopgSyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через psycopg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    conn_proxy = providers.Factory(psycopg_proxy.PsycopgConnectionProxy, pg_config)
    sql_creator = providers.Factory(PsycopgRawSQLCreator)
    psycopg_repository = providers.Factory(
        psycopg_repository.PsycopgSyncRepository, conn_proxy, sql_creator
    )
    psycopg_uow = providers.Factory(psycopg_uow.PsycopgSyncUOW, psycopg_repository)


class PsycopgAsyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для асинхронной работы с БД Postgres через psycopg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(packages=["web.entrypoints"])

    conn_proxy = providers.Factory(psycopg_proxy.PsycopgAsyncConnectionProxy, pg_config)
    sql_creator = providers.Factory(PsycopgRawSQLCreator)
    psycopg_repository = providers.Factory(
        psycopg_repository.PsycopgAsyncRepository, conn_proxy, sql_creator
    )
    psycopg_uow = providers.Factory(psycopg_uow.PsycopgAsyncUOW, psycopg_repository)
