import fastapi
import uvicorn

from config import app_config
from config import uvicorn_config
from tools import di_container
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
        default_response_class=fastapi.responses.ORJSONResponse
    )

    return fastapi_app


app = create_app()
router_registrator.register_routers(app)

if __name__ == "__main__":
    session_container = di_container.DomainContainer()

    modules = [
        "services.oil_rate_calc_service"
    ]

    session_container.wire(modules=modules)

    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
