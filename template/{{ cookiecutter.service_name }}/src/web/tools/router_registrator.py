from fastapi import FastAPI

from web.entrypoints import oil_rate_calculator_entrypoint


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(oil_rate_calculator_entrypoint.router)