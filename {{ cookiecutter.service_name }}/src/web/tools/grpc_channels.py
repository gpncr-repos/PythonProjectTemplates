import grpc

from config import app_config
from interfaces import base_grpc_channel

app_config = app_config.app_config


class IndexChannel(base_grpc_channel.GRPCChannel):
    """
    Канал grpc для пакета index
    """

    _channel = grpc.insecure_channel(app_config.get_grpc_address())