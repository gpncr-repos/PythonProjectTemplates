import fastapi
import uvicorn

from config import app_config
from config import uvicorn_config

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

if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
