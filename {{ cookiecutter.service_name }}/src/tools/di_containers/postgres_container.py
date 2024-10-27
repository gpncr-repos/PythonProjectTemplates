# thirdparty
from dependency_injector import containers, providers

# project
from config.pg_config import pg_config
from storage.psycopg import psycopg_connection
from repositories import psycopg_repository


class PsycopgSyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через psycopg
    """

    wiring_config = containers.WiringConfiguration(packages=["web.entrypoints"])

    psycopg_conn = providers.Factory(psycopg_connection.PsycopgSyncConnection, pg_config)
    psycopg_repository = providers.Factory(psycopg_repository.PsycopgSyncRepository, psycopg_conn)


class PsycopgAsyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для асинхронной работы с БД Postgres через psycopg
    """

    wiring_config = containers.WiringConfiguration(packages=["web.entrypoints"])

    psycopg_conn = providers.Factory(psycopg_connection.PsycopgAsyncConnection, pg_config)
    psycopg_repository = providers.Factory(psycopg_repository.PsycopgAsyncRepository, psycopg_conn)
