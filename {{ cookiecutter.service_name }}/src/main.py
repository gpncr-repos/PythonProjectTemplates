import uvicorn

from config import uvicorn_config
from web.tools import fastapi_initializer

app = fastapi_initializer.app


if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
