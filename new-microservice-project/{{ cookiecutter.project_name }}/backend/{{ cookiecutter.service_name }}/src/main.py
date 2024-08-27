import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, responses

from config.settings import Settings
from di import AppProvider
from web.controllers.index import router

settings = Settings()

def create_fastapi_app():
    app = FastAPI(
        default_response_class=responses.ORJSONResponse,
        debug=True if settings.okd_stage == "DEV" else False,
        title=settings.service_name,
        version=settings.service_version,
    )
    app.include_router(router)
    return app

def create_di_app():
    app = create_fastapi_app()
    container = make_async_container(AppProvider(), context={Settings: settings})
    setup_dishka(container, app)
    return app


if __name__ == '__main__':
    uvicorn.run(
        "main:create_di_app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True if settings.okd_stage == "DEV" else False,
    )
