# Подключение к Postgres через ORM SQLAlchemy

Подключение к БД Postgres реализовано через ORM SQLAlchemy в синхронном и асинхронном режиме.
Конфиг postgres находится в **config/pg_config.py**.

## Подключение к Базе Данных

### Прокси-соединение

Предоставляется интерфейс **ConnectionProxy** из **interfaces/base_proxy.py** для синхронных и асинхронных подключений к базе данных PostgreSQL. Прокси-соединение принимает в качестве аргументов фабрику движков для подключения к БД.

Основные методы:
- `connect()`: Устанавливает соединение и возвращает объект сессии Алхимии.
- `disconnect()`: Возвращает сессию в пул соединений движка.

Как только объект сессии был получен пользователем, работа с ним сводится к операциям, согласно документации библиотеки SQLAlchemy.

## Движок для подключения к БД

Для управления соединением с базой данных используется движок, реализованный через фабрику. Движок доступен как в синхронном, так и в асинхронном вариантах.
Его реализация находится в директории **tools/factories/alchemy_engine_factory.py**.

## Репозиторий

Предлагается реализация репозитория, совместимого как с синхронными, так и с асинхронными подходами, который реализует интерфейс **BaseRepository** из **interfaces/base_repository.py**.
Базовый класс репозитория находится в директории **repositories/base_alchemy_repository.py**.

## Unit of Work (UOW)

Для обеспечения транзакционности работы с базой данных PostgreSQL были написаны два класса Unit of Work (UOW) для синхронной и асинхронной реализаций.

Класс UOW функционирует как контекстный менеджер и в методе `__exit__()` вызывает:
- `commit()`: для подтверждения транзакции.
- `rollback()`: для отката транзакции в случае возникновения исключений.

## DI-контейнер

Для инициализации объекта UOW и работы с базой данных PostgreSQL используется DI-контейнер.
Пример создания объектов в DI-контейнере:

```python
    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=[])

    engine_factory = providers.Singleton(
        alchemy_engine_factory.AlchemySyncEngineFactory,
        config.postgres_dsn,
        config.connection_pool_size,
    )
    connection_proxy = providers.Factory(
        connection_proxy.AlchemySyncConnectionProxy, engine_factory
    )

    # Добавить провайдеры конкретных реализаций репозиториев
    repository = providers.Factory(
        base_alchemy_repository.TestSyncRepo, connection_proxy
    )

    # Добавить провайдеры конкретных реализаций UOW
    uow = providers.Factory(alchemy_uow.AlchemySyncUOW, repository)
```

Сначала создается соответствующий движок для подключения к БД, который является Синглтоном и будет использоваться на протяжении жизни всего приложения. Движок передается в прокси-соединение.

Далее задаются репозитории и UOW, в которые они прокидываются.

В асинхронном варианте используется аналогичная цепочка создания объектов.

## Пример использования psycopg UOW через DI-контейнер


```python
# some code

@inject
def psycopg_example(
    uow: AlchemySyncUOW = Provide[AlchemySyncContainer.uow]
):
    with uow as u:
        u.repository.create(...)
        u.commit()

# some code

container = AlchemySyncContainer()
engine = container.engine_factory().create()
engine.dispose()
```

Особое внимание в этом примере надо обратить на явное закрытие соединения с БД пользователем через объект движка и на метод `create()`. Несмотря на название, он возвращает один и тот же движок, т.к. фабрика движков является Синглотоном.
