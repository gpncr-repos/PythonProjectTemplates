from dependency_injector import containers, providers

from interfaces import base_http_session_maker
from repositories import http_repository
from uows import http_uow


class HTTPIntegrationContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами HTTP-интеграции
    """

    wiring_config = containers.WiringConfiguration(modules=...)

    http_sync_session = providers.Factory(base_http_session_maker.HTTPSyncSessionMaker)
    http_async_session = providers.Factory(base_http_session_maker.HTTPAsyncSessionMaker)

    http_sync_repository = providers.Factory(
        http_repository.SyncHTTPRepository, http_sync_session
    )
    http_async_repository = providers.Factory(
        http_repository.SyncHTTPRepository, http_async_session
    )

    http_sync_uow = providers.Factory(
        http_uow.SyncHTTPUOW, http_sync_repository
    )
    http_async_uow = providers.Factory(
        http_uow.AsyncHTTPUOW, http_async_repository
    )