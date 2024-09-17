from fastapi import FastAPI

from web.entrypoints import index_entrypoint


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(index_entrypoint.router)