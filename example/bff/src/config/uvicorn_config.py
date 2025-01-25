from config import app_config, logger_config

config = app_config.app_config

uvicorn_config = {
    "host": config.app_host,
    "port": config.app_port,
    "log_level": "debug" if config.okd_stage == "DEV" else "info",
    "reload": True,
    "interface": "auto",
    "log_config": logger_config.get_json_output_logging_config()
}
