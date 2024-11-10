# Кеширование Redis

Кеширование данных реализовано с помощью Redis и написанных к нему репозитория с UOW.
Конфиг Redis находится в **config/redis_config.py**.

## Соединение

Синхронное и асинхронное соединения реализуют имеют общий метод `get_connection()`, который возвращает объект соединения.
Реализации сессий представлены в модуле **session.py** директории **storage/sqlalchemy**.

## Репозиторий

Для работы с хранилищем Redis было реализовано 2 репозитория - для синхронной и асинхронной реализаций. Они находятся в **repositories/redis_repository.py**. В инициализоре соответствующий репозиторий получает переданный объект соединения, с которым он в дальнейшем будет работать.

## UOW

Для работы с хранилищем Redis было реализовано 2 UOW - для синхронной и асинхронной реализаций.
В данной реализации Redis не поддерживает транзакционность, поэтому UOW используется для удобного закрытия соединения, делая это за пользователя. UOW реализован в виде контекстного менеджера, который в методе `__exit__()` вызывает `close()` у объекта соединения, который передается из репозитория. Методы `commit()` и `rollback()` UOW остались нереализованными.

## DI-контейнер

Для инициализации объекта UOW и дальнейшей работы с хранилищем Redis соблюдается следующая цепочка создания объектов в di-контейнере:

```python
redis_settings = providers.Singleton(redis_config.RedisConfig)
redis_sync_conn = providers.Factory(
    redis_connection.RedisConnection, redis_settings
)
redis_sync_repository = providers.Factory(
    redis_repository.SyncRedisRepository, redis_sync_conn
)
redis_sync_uow = providers.Factory(redis_uow.SyncRedisUOW, redis_sync_repository)
```

Изначально создается объект настроек, который затем передается в объект соединения. Как только был получен объект соединения, инициализируется объект репозитория, который является аргументов для инициализатора объекта UOW.

## Работа с UOW

Работа с UOW ведется без использования методов `commit()` и `rollback()`:

```python
# some code

with uow:
    some_obj = uow.repository.retrieve(...)

# some code
```