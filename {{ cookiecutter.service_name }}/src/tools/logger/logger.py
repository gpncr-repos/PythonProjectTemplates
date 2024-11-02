import datetime
import json
import logging.handlers
from inspect import Traceback

from pythonjsonlogger import jsonlogger

from config import app_config
from tools.globals import g
from tools.logger import params

config = app_config.app_config
logger = logging.getLogger("utils-logger")


class LogLevelFilter(logging.Filter):
    """
    Класс фильтра по уровлю лога
    """

    def __init__(self, logs_level: int) -> None:
        """
        Инициализировать переменные
        :param logs_level: уровень лога
        """

        self.logs_level = logs_level
        super().__init__()

    def filter(self, record: any) -> bool:
        """
        Проверить, соответствует ли уровень лога записи установленному
        :return: True, если уровень лога записи соответствует установленному, иначе - False
        """

        return record.levelno >= self.logs_level


class ExtraLoggerAdapter(logging.LoggerAdapter):
    """
    Декоратор для логгера, который добавляет extra для всех лог-записей.

    Пример использования:
    logger = ExtraLoggerAdapter(logger, extra={"new_extra_field": "value_extra_field"})
    """

    def process(self, msg: str, kwargs: dict) -> tuple[str, dict]:
        """
        Обработать сообщение и его дополнительные параметры
        :param msg: сообщение
        :param kwargs: дополнительные параметры
        """

        if "extra" not in kwargs:
            kwargs["extra"] = {}

        kwargs["extra"].update(self.extra)

        return msg, kwargs


class CustomJSONFormatter(jsonlogger.JsonFormatter):
    """
    Форматтер для добавления поля msg в выходной json
    """

    def _get_extra_context_info(self) -> dict:
        """
        Получить дополнительные поля из глобальной переменной
        :return: словарь с дополнительными полями
        """

        extra_info = {}

        if "extra_info_for_logs" in g._vars and g.extra_info_for_logs is not None:
            extra_info.update(g.extra_info_for_logs)

        return extra_info

    def jsonify_log_record(self, log_record: dict[str, any]) -> str:
        """
        Преобразовать лог к формату JSON
        :param log_record: информация о логе
        :return: строка в формате JSON
        """
        log_record_sorted = dict(sorted(log_record.items()))

        return self.json_serializer(
            log_record_sorted,
            default=self.json_default,
            cls=self.json_encoder,
            indent=self.json_indent,
            ensure_ascii=self.json_ensure_ascii
        )

    def add_fields(self, log_record: dict[str, any], record: logging.LogRecord, message_dict: dict[str, any]) -> None:
        """
        Добавить поля в лог
        :param log_record: пустой словарь для заполнения доп полями с информацией о логе
        :param record: информация о логе
        :param message_dict: словарь сообщений о логе
        """

        super().add_fields(log_record, record, message_dict)

        extra_fields = self._get_extra_context_info()

        message = log_record["message"] if not extra_fields.get("err_msg") else f"Ошибка: {extra_fields.get('err_msg')}"

        log_record["asctime"] = datetime.datetime.utcfromtimestamp(record.created)
        log_params_model = params.CustomLogParams(
            system_log_type = "user" if "user_id" in extra_fields else "application",
            user_id=extra_fields.get("user_id"),
            session_id=extra_fields.get("session_id"),
            project_name=config.project_name,
            level=record.levelname,
            message=message
            if "req_method" not in extra_fields or record.levelname == "ERROR"
            else "Обработан HTTP-запрос",
            request=extra_fields.get("method"),
            http_referrer=extra_fields.get("url"),
            response_status=extra_fields.get("response_status"),
            request_body=extra_fields.get("request_body"),
            response_body=extra_fields.get("response_body")
        )
        log_record["msg"] = message

        del log_record["message"]

        if log_record.get("color_message"):
            del log_record["color_message"]

        log_record["logger"] = {}
        log_record["logger"]["name"] = record.name
        log_record["logger"]["level"] = record.levelname

        log_params = log_params_model.to_dict()
        log_record.update(log_params)


class ExtraFormatter(CustomJSONFormatter):
    """
    Форматтер для логов с доп полями
    """

    COMMON_RECORD_ATTRS = [
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack",
        "tags",
        "thread",
        "threadName",
        "stack_info",
        "asctime",
        "extra",
        "extra_info",
        "report"
    ]

    def serialize_log_record(self, log_record: dict[str, any]) -> dict[str, any]:
        """
        Сериализовать лог.
        В данном случае просто возвращаем информацию о логе
        :param log_record: информация о логе
        :return: информация о логе
        """

        return log_record

    def formatException(self, ei: tuple[type[BaseException], BaseException, Traceback | None]) -> str:
        """
        Отформатировать исключение и вернуть в виде строки
        :param ei: информация об исключении
        :return: отформатированная строка
        """

        result = super().formatException(ei)

        return result

    def format(self, record: logging.LogRecord) -> str:
        """
        Отформатировать лог и вернуть строку
        :param record: метаднные о логе
        :return: отформатированная строка
        """

        s: dict[str, any] = super().format(record)

        message = (
            f"{datetime.datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')} {record.levelname} {s['msg']}"
        )

        if record.exc_info:
            message += "\n" + self.formatException(record.exc_info)

        if s.get("debug_info"):
            message += f"\ndebug_info: {json.dumps(s['debug_info'], ensure_ascii=False, default=str)}"

        extra = {key: value for key, value in record.__dict__.items() if key not in self.COMMON_RECORD_ATTRS}
        extra.update(self._get_extra_context_info())

        if extra:
            message += f"\nextra: {json.dumps(extra, ensure_ascii=False, default=str)}"

        record.message = message

        return super().serialize_log_record(record.__dict__)
