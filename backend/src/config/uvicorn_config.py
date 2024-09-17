from config import app_config

config = app_config.app_config

uvicorn_config = {
    "host": config.app_host,
    "port": config.app_port,
    "log_level": "info",
    "reload": True,
    "interface": "auto"
}
