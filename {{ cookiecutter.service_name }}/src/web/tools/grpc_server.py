from concurrent import futures

from grpc import aio

from config import app_config

app_config = app_config.app_config

server = aio.server(futures.ThreadPoolExecutor(max_workers=app_config.grpc_workers_count))
server.add_insecure_port(app_config.get_grpc_address())
