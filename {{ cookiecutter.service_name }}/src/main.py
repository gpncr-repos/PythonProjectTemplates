from dependency_injector import providers
import uvicorn

from config import uvicorn_config
{% if cookiecutter.api_architecture == "grpc" %}
from protobufs import index_pb2_grpc
from tools.di_containers import stub_di_container
{% endif %}
from web.tools import fast_api_initializer, router_registrator
{% if cookiecutter.api_architecture == "grpc" %}
index_stub_container = stub_di_container.IndexStubContainer()
channel = index_stub_container.channel()
index_stub_container.stub.override(
    providers.Factory(
        index_pb2_grpc.IndexServiceStub,
        channel=channel.get_channel()
    )
)
{% endif %}
app = fast_api_initializer.initiliaze_app()
router_registrator.register_routers(app)

if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
