import abc

import grpc


class GRPCChannel(abc.ABC):
    """
    Базовый класс канала grpc
    """

    _channel: grpc.Channel

    def get_channel(self) -> grpc.Channel:
        """
        Получить канал grpc
        :return: канал grpc
        """

        return self._channel
