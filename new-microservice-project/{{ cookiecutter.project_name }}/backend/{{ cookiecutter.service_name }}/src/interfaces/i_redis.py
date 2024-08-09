from abc import ABC, abstractmethod
from config.db_settings import RedisSettings


class IRedis(ABC):

    def __init__(self, settings: RedisSettings) -> None:
        self.settings = settings

    @abstractmethod
    def get_client(self):
        raise NotImplementedError

    @abstractmethod
    def set_cache(self, key, value, ttl):
        raise NotImplementedError

    @abstractmethod
    def get_cache(self, key):
        raise NotImplementedError

    @abstractmethod
    def delete_keys(self, keys: list):
        raise NotImplementedError
