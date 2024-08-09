import datetime
import logging
import uuid
from typing import Optional, Union

import orjson
from redis import asyncio as aioredis

from config.db_settings import RedisSettings
from interfaces import IRedis


class RedisAsync(IRedis):
    __CLIENT = None

    def __init__(self, settings: RedisSettings) -> None:
        super().__init__(settings)

    async def get_client(self) -> aioredis.Redis:
        if not self.__CLIENT:
            self.__CLIENT = await aioredis.from_url(self.settings.dns)
        return self.__CLIENT

    async def __set_cache(self, key, value: bytes, ttl: int):
        try:
            redis = await self.get_client()
            if value:
                await redis.set(key, value, ex=ttl)
            else:
                await self.delete_keys([key])
        except aioredis.RedisError as ex:
            logging.exception(ex)

    async def set_cache(self, key, value: Union[list, dict, object], ttl: Optional[int] = None):
        if value:
            await self.__set_cache(key, self.to_json(value), ttl)

    async def __get_cache(self, key):
        try:
            redis = await self.get_client()
            value = await redis.get(key)
        except aioredis.RedisError as ex:
            logging.exception(ex)
            value = None

        return value

    async def get_cache(self, key):
        value = await self.__get_cache(key)
        if value:
            return orjson.loads(value)

    async def __delete_keys(self, keys: list):
        try:
            redis = await self.get_client()
            for key in keys:
                await redis.delete(key)
        except aioredis.RedisError as ex:
            logging.exception(ex)

    async def delete_keys(self, keys: list):
        if keys:
            await self.__delete_keys(keys)

    def to_json(self, obj) -> bytes:
        return orjson.dumps(obj, default=self.__default, option=orjson.OPT_NON_STR_KEYS)

    @staticmethod
    def __default(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
