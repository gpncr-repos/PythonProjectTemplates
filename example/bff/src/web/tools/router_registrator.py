from fastapi import FastAPI

from config import app_config
from web.entrypoints import index_entrypoint

app_config = app_config.app_config


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(index_entrypoint.router, prefix=f"/api/{app_config.app_version}")
