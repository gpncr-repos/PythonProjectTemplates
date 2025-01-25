from copy import deepcopy

from config import app_config

config = app_config.app_config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": "tools.logger.logger.CustomJSONFormatter",
            "json_ensure_ascii": False
        },
        "extended_formatter": {
            "()": "tools.logger.logger.ExtraFormatter",
            "json_ensure_ascii": False
        }
    },
    "handlers": {
        "console_json_handler": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
            "stream": "ext://sys.stdout"
        },
        "console_extended_handler": {
            "class": "logging.StreamHandler",
            "formatter": "extended_formatter",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [],
        "filters": [],
        "propagate": True
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": [],
            "filters": [],
            "propagate": False
        }
    },
    "filters": {
        "debugFilter": {
            "()": "tools.logger.logger.LogLevelFilter",
            "logs_level": 10
        },
        "infoFilter": {
            "()": "tools.logger.logger.LogLevelFilter",
            "logs_level": 20
        },
        "errorFilter": {
            "()": "tools.logger.logger.LogLevelFilter",
            "logs_level": 40
        }
    }
}


def get_raw_output_logging_config() -> dict:
    logger_config = deepcopy(LOGGING)

    logger_config["root"]["handlers"].extend(["console_extended_handler"])
    logger_config["root"]["filters"].extend(["debugFilter"])

    logger_config["loggers"]["uvicorn"]["handlers"].extend(["console_extended_handler"])

    return logger_config


def get_json_output_logging_config() -> dict:
    logger_config = deepcopy(LOGGING)

    logger_config["root"]["handlers"].append("console_json_handler")
    logger_config["loggers"]["uvicorn"]["handlers"].append("console_json_handler")

    if config.okd_stage == "DEV":
        logger_config["root"]["filters"].append("infoFilter")
        logger_config["loggers"]["uvicorn"]["filters"].append("debugFilter")
    else:
        logger_config["root"]["filters"].append("debugFilter")
        logger_config["loggers"]["uvicorn"]["filters"].append("infoFilter")

    return logger_config
