from protobufs import index_pb2, index_pb2_grpc

from config import app_config

app_config = app_config.app_config


class IndexServicer(index_pb2_grpc.IndexServiceServicer):
    """
    Сервис для формирования общей информации о приложении
    """

    def GetInfo(self, request, context) -> index_pb2.IndexResponse:
        """
        Получить информацию о приложении
        :param request: ...
        :param context: ...
        :return: информация о приложении
        """

        return index_pb2.IndexResponse(
            project_name=app_config.project_name,
            app_name=app_config.app_name,
            app_version=app_config.app_version
        )
