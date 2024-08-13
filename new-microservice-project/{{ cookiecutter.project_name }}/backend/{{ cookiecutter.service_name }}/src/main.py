import uvicorn
from fastapi import FastAPI, responses

from config.settings import settings, Settings
from web.controllers.main import router


def create_fastapi_app():
    app = FastAPI(
        default_response_class=responses.ORJSONResponse,
        debug=True if settings.okd_stage == "DEV" else False,
        title=settings.service_name,
        description="Сервисная модель",
        version=settings.service_version,
    )
    app.include_router(router)
    return app


if __name__ == '__main__':
    uvicorn.run(
        "main:create_app",
        host=settings.app_host,
        port=settings.app_port,
    )
