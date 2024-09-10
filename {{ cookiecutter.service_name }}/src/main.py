import fastapi
import uvicorn

from config import fastapi_config


def create_app() -> fastapi.FastAPI:
    """
    Инициализировать приложение FastAPI
    """

    fastapi_app = fastapi.FastAPI()

    return fastapi_app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", **fastapi_config.config)
