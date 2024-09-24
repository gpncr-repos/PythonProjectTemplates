import uvicorn

from config import app_config, uvicorn_config
from web.tools import fastapi_initializer, router_registrator

app_config = app_config.app_config

app = fastapi_initializer.initiliaze_app()
router_registrator.register_routers(app)

if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
