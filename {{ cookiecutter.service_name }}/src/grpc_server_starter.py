import asyncio
import sys

from web.tools import grpc_server, service_registrator

grpc_server = grpc_server.server
service_registrator.register_services(grpc_server)


async def run_grpc_server() -> None:
    """
    Запустить grpc-сервер
    """

    try:
        await grpc_server.start()
        await grpc_server.wait_for_termination()
    except KeyboardInterrupt:
        grpc_server.stop(0)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_grpc_server())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
