# thirdparty
# project
from config.pg_config import pg_config
from dependency_injector import containers, providers
from repositories import psycopg_repository
from repositories.sql_tools import PsycopgRawSQLCreator
from storage.psycopg import psycopg_connection


class PsycopgSyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через psycopg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    psycopg_conn = providers.Factory(psycopg_connection.PsycopgSyncConnection, pg_config)
    sql_creator = providers.Factory(PsycopgRawSQLCreator)
    psycopg_repository = providers.Factory(
        psycopg_repository.PsycopgSyncRepository, psycopg_conn, sql_creator
    )


class PsycopgAsyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для асинхронной работы с БД Postgres через psycopg
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    psycopg_conn = providers.Factory(psycopg_connection.PsycopgAsyncConnection, pg_config)
    sql_creator = providers.Factory(PsycopgRawSQLCreator)
    psycopg_repository = providers.Factory(
        psycopg_repository.PsycopgAsyncRepository, psycopg_conn, sql_creator
    )
