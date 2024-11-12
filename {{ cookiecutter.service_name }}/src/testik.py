import uuid

from dependency_injector import providers
from repositories.tools import psycopg_cursor_proxies
from tools.di_containers import postgres_container

container = postgres_container.PsycopgSyncContainer()
container.cursor_type.override(providers.Factory(psycopg_cursor_proxies.ClientPsycopgCursorProxy))

with container.psycopg_uow() as uow:
    uow.repository.create("test1", {"id": uuid.uuid4(), "col1": "record1"})
    uow.commit()
