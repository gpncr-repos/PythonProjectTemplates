import fastapi
import uvicorn

from config import app_config
from config import uvicorn_config
from tools.di_containers import domain_di_container, service_di_container
from web.tools import router_registrator

app_config = app_config.app_config


def create_app() -> fastapi.FastAPI:
    """
    Инициализировать приложение FastAPI
    """

    fastapi_app = fastapi.FastAPI(
        title=app_config.project_name,
        version=app_config.app_version,
        debug=True if app_config.okd_stage == "DEV" else False,
        default_response_class=fastapi.responses.JSONResponse
    )

    return fastapi_app


app = create_app()

domain_container = domain_di_container.DomainContainer()
service_container = service_di_container.ServiceContainer()

app.domain_container = domain_container
app.service_container = service_container

router_registrator.register_routers(app)

if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
