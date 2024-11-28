import asyncio

from dependency_injector import providers
from storage.raw_postgres import asyncpg_cursor_proxies, psycopg_cursor_proxies
from tools.di_containers import raw_postgres_container

# CREATE TABLE IF NOT EXISTS users (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     phone VARCHAR(15) NOT NULL
# );

users = [
    {"name": "Sam", "phone": "32283228"},
    {"name": "Tom", "phone": "88005553535"},
    {"name": "Mike", "phone": "4242"},
]

insert_sql = """
        INSERT INTO users (name, phone) VALUES ($1, $2)
"""

insert_psy_sql = """
        INSERT INTO users (name, phone) VALUES (%s, %s)
"""

delete_sql = """
    DELETE FROM users
    WHERE name = $1
"""

delete_psy_sql = """
    DELETE FROM users
    WHERE name = %s
"""

select_sql = """
    SELECT *
    FROM users u
    WHERE u.name != $1
"""

select_psy_sql = """
    SELECT *
    FROM users u
    WHERE u.name != %s
"""

select_one_sql = """
    SELECT *
    FROM users u
    WHERE u.name = $1
"""

select_one_psy_sql = """
    SELECT *
    FROM users u
    WHERE u.name = %s
"""

update_sql = """
    UPDATE users
    SET phone = $1
    WHERE name = $2
"""

update_psy_sql = """
    UPDATE users
    SET phone = %s
    WHERE name = %s
"""

container = raw_postgres_container.PsycopgSyncContainer()
container.cursor_type.override(providers.Factory(psycopg_cursor_proxies.ClientPsycopgCursorProxy))


async_container = raw_postgres_container.AsyncpgContainer()
async_container.cursor_type.override(
    providers.Factory(asyncpg_cursor_proxies.ClientAsyncpgCursorProxy)
)


def delete():
    with container.psycopg_uow() as uow:
        for user in users:
            uow.repository.delete(delete_psy_sql, params=[user["name"]])
        uow.commit()


def create():
    with container.psycopg_uow() as uow:
        for user in users:
            uow.repository.create(insert_psy_sql, params=list(user.values()))
        uow.commit()


def get_list():
    with container.psycopg_uow() as uow:
        return uow.repository.list(select_psy_sql, 3, ["Ted"])


def get_one():
    with container.psycopg_uow() as uow:
        return uow.repository.retrieve(select_one_psy_sql, ["Sam"])


def update():
    with container.psycopg_uow() as uow:
        return uow.repository.update(update_psy_sql, ["9999999", "Sam"])


async def async_delete():
    async with async_container.asyncpg_uow() as uow:
        for user in users:
            await uow.repository.delete(delete_sql, params=[user["name"]])
        await uow.commit()


async def async_create():
    async with async_container.asyncpg_uow() as uow:
        for user in users:
            await uow.repository.create(insert_sql, params=user.values())
        await uow.commit()


async def async_get_list():
    async with async_container.asyncpg_uow() as uow:
        return await uow.repository.list(select_sql, 3, ["Ted"])


async def async_get_one():
    async with async_container.asyncpg_uow() as uow:
        return await uow.repository.retrieve(select_one_sql, ["Sam"])


async def async_update():
    async with async_container.asyncpg_uow() as uow:
        return await uow.repository.update(update_sql, ["9999999", "Sam"])


async def main():
    delete()
    create()
    get_list()
    get_one()
    update()

    global container
    container.cursor_type.override(
        providers.Factory(psycopg_cursor_proxies.ServerPsycopgCursorProxy)
    )

    # delete()
    # create()
    get_list()
    get_one()
    # update()

    await async_delete()
    await async_create()
    await async_get_list()
    await async_get_one()
    await async_update()

    global async_container
    async_container.cursor_type.override(
        providers.Factory(asyncpg_cursor_proxies.ServerAsyncpgCursorProxy)
    )

    await async_delete()
    await async_create()
    await async_get_list()
    await async_get_one()
    await async_update()


asyncio.run(main())
