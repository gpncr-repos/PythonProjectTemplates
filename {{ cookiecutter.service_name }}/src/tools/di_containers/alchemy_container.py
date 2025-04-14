from dependency_injector import containers, providers

from config import pg_config
from repositories import base_alchemy_repository
from storage.sqlalchemy import connection_proxy
from tools.factories import alchemy_engine_factory
from uows import alchemy_uow

config = pg_config.pg_config


class AlchemySyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через синхронную сессию Алхимии
    """

    # Указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    engine_factory = providers.Singleton(
        alchemy_engine_factory.AlchemySyncEngineFactory,
        config.postgres_dsn,
        config.connection_pool_size,
    )
    connection_proxy = providers.Factory(
        connection_proxy.AlchemySyncConnectionProxy, engine_factory
    )

    # Добавить провайдеры конкретных реализаций репозиториев
    repository = providers.Factory(
        base_alchemy_repository.BaseAlchemyRepository, connection_proxy
    )

    # Добавить провайдеры конкретных реализаций UOW
    uow = providers.Factory(alchemy_uow.AlchemySyncUOW, repository)


class AlchemyAsyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через асинхронную сессию Алхимии
    """

    # Указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    engine_factory = providers.Singleton(
        alchemy_engine_factory.AlchemyAsyncEngineFactory,
        config.postgres_async_dsn,
        config.connection_pool_size,
    )
    connection_proxy = providers.Factory(
        connection_proxy.AlchemyAsyncConnectionProxy, engine_factory
    )

    # Добавить провайдеры конкретных реализаций репозиториев
    repository = providers.Factory(
        base_alchemy_repository.BaseAlchemyRepository, connection_proxy
    )

    # Добавить провайдеры конкретных реализаций UOW
    uow = providers.Factory(alchemy_uow.AlchemyAsyncUOW, repository)
