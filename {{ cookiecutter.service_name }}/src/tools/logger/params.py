import dataclasses
from typing import Literal


@dataclasses.dataclass
class CustomLogParams:
    """
    Класс, содержащий поля для логирования
    """

    # Добавить свои поля класса как поля для вывода в лог

    # Тип лога
    system_log_type: Literal["user", "application"] = "application"

    # Идентификатор пользователя
    user_id: str | None = None

    # Идентификатор сессии
    session_id: str | None = None

    # Название проекта
    project_name: str | None = None

    # Уровень лога
    level: str | None = None

    # Детальное сообщение
    message: str | None = None

    # Статус события
    status: str | None = None

    # Метод HTTP
    request: str | None = None

    # URL запроса
    http_referrer: str | None = None

    # Код статуса овтета API
    response_status: str | None = None

    # Тело запроса для статусов 4**, 5**
    request_body: bytes | str | dict | list | None = None

    # Тело ответа для статусов 4**, 5**
    response_body: bytes | str | dict | list | None = None

    def to_dict(self, exclude_none: bool = False) -> dict:
        """
        Преобразовать поля класса в словарь
        :param exclude_none: исключить поля, значение которых равно None
        :return: словарь полей класса
        """

        if exclude_none:
            return {
                key: value
                for key, value in dataclasses.asdict(self).items() if value
            }

        return dataclasses.asdict(self)


@dataclasses.dataclass
class CustomLogParamsExtended(CustomLogParams):
    """
    Класс, дополняющий описание логов полезными для сервиса полями
    """

    process_name: str | None = None
    thread_name: str | None = None
