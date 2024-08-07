from abc import ABC, abstractmethod
from config import DBSettings


class ISqlAlchemy:

    def __init__(self, pg_settings: DBSettings) -> None:
        self.pg_settings = pg_settings

    @abstractmethod
    def Session(self):  # noqa
        raise NotImplementedError

    @abstractmethod
    def get_db(self):
        raise NotImplementedError

    @abstractmethod
    def __build_engine(self):
        raise NotImplementedError
