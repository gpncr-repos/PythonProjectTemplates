from dependency_injector import containers, providers

from protobufs import index_pb2, index_pb2_grpc
from web.tools import grpc_channels


class IndexStubContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами объектов стабов grpc для пакета index
    """

    wiring_config = containers.WiringConfiguration(modules=["web.entrypoints.index_entrypoint"])

    channel = providers.Singleton(grpc_channels.IndexChannel)
    stub = providers.Factory(index_pb2_grpc.IndexServiceStub)
    response = providers.Factory(index_pb2.IndexResponse)
