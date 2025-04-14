import fastapi

from config import app_config
from web.middlewares import logger_middleware
from web.tools import router_registrator

app_config = app_config.app_config


def initiliaze_app() -> fastapi.FastAPI:
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

app = initiliaze_app()
router_registrator.register_routers(app)

app.add_middleware(logger_middleware.LogRequestInfoMiddleware)
app.add_middleware(logger_middleware.SetRequestContextMiddleware)
