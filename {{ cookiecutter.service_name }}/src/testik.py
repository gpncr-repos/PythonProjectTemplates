import asyncio

from dependency_injector import providers
from storage.raw_postgres import asyncpg_cursor_proxies
from tools.di_containers import raw_postgres_container

# container = postgres_container.PsycopgSyncContainer()
# container.cursor_type.override(providers.Factory(psycopg_cursor_proxies.ClientPsycopgCursorProxy))
# a = container.connection_pool()
# b = container.dsn()
# c = container.cursor_type()
# d = container.connection_proxy()
# e = container.psycopg_repository()
# f = container.psycopg_uow()

# with container.psycopg_uow() as uow:
#     uow.repository.create("test1", {"id": uuid.uuid4(), "col1": "record1"})
#     uow.commit()


container = raw_postgres_container.AsyncpgContainer()
container.cursor_type.override(providers.Factory(asyncpg_cursor_proxies.ServerAsyncpgCursorProxy))


async def run():
    async with container.asyncpg_uow() as uow:
        gen = await uow.repository.list(
            """
            select *
            from test
            """,
            2,
        )
        async for a in gen:
            ...


asyncio.run(run())
