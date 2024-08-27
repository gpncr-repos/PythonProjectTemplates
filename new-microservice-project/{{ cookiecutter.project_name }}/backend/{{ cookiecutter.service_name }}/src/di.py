# stdlib
from typing import AsyncIterable

# thirdparty
from dishka import Provider, provide, Scope, from_context
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis

# project
from config.settings import Settings
from interfaces.cache import RedisCacheRepository
from interfaces.repository import AbstractAlchemyRepository
from tools.factories.alchemy_session_factory import AlchemyAsyncSession
from tools.factories.redis_connection_factory import RedisAsyncConnection


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_session_factory(self, settings: Settings) -> AlchemyAsyncSession:
        return AlchemyAsyncSession(settings)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: AlchemyAsyncSession) -> AsyncIterable[AsyncSession]:
        yield session_factory()

    @provide(scope=Scope.REQUEST)
    async def get_repository(self, sa_session: AsyncSession) -> AbstractAlchemyRepository:
        return AbstractAlchemyRepository(session=sa_session)

    @provide(scope=Scope.REQUEST)
    async def get_connection_factory(self, settings: Settings) -> RedisAsyncConnection:
        return RedisAsyncConnection(settings)

    @provide(scope=Scope.REQUEST)
    async def get_redis_conn(self, conn_factory: RedisAsyncConnection) -> aioredis.Redis:
        return await conn_factory()

    @provide(scope=Scope.REQUEST)
    async def get_redis_cache_repo(self, connection: aioredis.Redis) -> RedisCacheRepository:
        return RedisCacheRepository(connection)
