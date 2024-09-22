from protobufs import index_pb2_grpc
from services import index_service


def register_services(server) -> None:
    """
    Зарегистрировать сервисы
    """

    index_pb2_grpc.add_IndexServiceServicer_to_server(index_service.IndexServicer(), server)
