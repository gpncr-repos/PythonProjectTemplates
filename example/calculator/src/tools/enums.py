import enum


class EDAType(enum.Enum):
    """
    Базовый Enum типы событий в EDA
    """

    pass


class CommandType(EDAType):
    """
    Enum типов команд
    """

    START_CALC = "START_CALC"


class EventType(EDAType):
    """
    Enum типов событий
    """

    CALC_STARTED = "CALC_STARTED"
    CALC_SUCCEED = "CALC_SUCCEED"
    CALC_FAILED = "CALC_FAILED"
