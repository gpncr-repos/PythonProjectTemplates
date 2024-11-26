# Подключение к Postgres через psycopg и asyncpg

Подключение к БД Postgres реализовано через psycopg в синхронном режиме и через asyncpg - в асинхронном.
Конфиг postgres находится в **config/pg_config.py**.


## Прокси-соединение

Синхронное и асинхронное подключение к бд Postgres реализует интерфейс **ConnectionProxy** из **interfaces/base_proxy.py**.
В качестве необходимых аргументов, прокси-соединение принимает прокси для получения курсора и фабрику пулов соединений. 
Для соединения с базой используется метод `connect()`. Он возвращает объект прокси-курсора, который был проинициализирован
соединением, полученным из пула.
Разрыв соединения с Postgres осуществляется пользователем с помощью метода `disconnect()` конкретного прокси. 

## Курсор

Курсор бд представлен в двух вариантах - клиентском и серверном. Оба реализуют интерфейс **BasePostgresCursorProxy** из 
**interfaces/base_postgres_cursor_proxy.py**. Инициализация курсора осуществляется методом `init_cursor()`.
За получения записей из базы отвечает метод  `retrieve_many()`.

## Пул соединений

Для получения соединения с бд, используется пул соединений. Получение пула осуществляется через фабрику. Фабрика пулов представлена
в синхронном и асинхронном вариантах. 


## Репозиторий
Для работы с базой данных используется репозиторий в синхронном и асинхронном исполнении, который реализует интерфейс
**BaseRepository** из **interfaces/base_repository.py**.
В качестве обязательного параметра репозиторий принимает объект прокси-соединения.
Методы репозитория, для совершения операций с базой данных, используют приватный метод `_execute_query()`. 
В нем осуществляется получение сохраненного в прокси-соединении объекта курсора. 
Для выполнения запроса к базе, курсор принимает sql-строку и необходимые параметры.

## Unit of work

Для обеспечения транзакционности при работе с бд Postgres через psycopg было реализовано 2 UOW - для синхронной и асинхронной реализаций.
UOW реализован в виде контекстного менеджера, который в методе `__exit__()` вызывает `commit()` у объекта соединения 
или `rollback()` при появлении исключения.

## DI-контейнер

Для инициализации объекта UOW и дальнейшей работы с бд Postgres через psycopg соблюдается следующая цепочка создания объектов в di-контейнере:

```python
connection_pool_factory = providers.Singleton(
    psycopg_connection_pool_factory.PsycopgPoolFactory,
    config.postgres_dsn,
    config.connection_pool_size,
)
cursor_type = providers.AbstractFactory(cursor_proxy.BasePsycopgCursorProxy)
connection_proxy = providers.Factory(
    connection_proxy.PsycopgConnectionProxy, connection_pool_factory, cursor_type
)
psycopg_repository = providers.Factory(
    psycopg_repository.PsycopgSyncRepository, connection_proxy
)
psycopg_uow = providers.Factory(psycopg_uow.PsycopgSyncUOW, psycopg_repository)
```

Сначала инициализируется фабрика пулов соединений которая принимает объект настроек.
Выбор типа курсора оставлен на пользователя. При настройке приложения требуется переопределить тип курсора на тот, 
что необходим пользователю. Пример:

```python
app = FastAPI()
container = raw_postgres_container.PsycopgSyncContainer()
container.cursor_type.override(providers.Factory(psycopg_cursor_proxies.ClientPsycopgCursorProxy))
app.container = container
```
Далее происходит получение прокси-соединения, которое принимает аргументами объекты фабрики пулов и прокси-курсора.
Как только был получен объект прокси-соединения, инициализируется объект репозитория, 
который является аргументов для инициализатора объекта UOW.

В асинхронном варианте с библиотекой asyncpg используется аналогичная цепочка создания объектов.

## Пример использования psycopg UOW через DI-контейнер


```python
# some code

@inject
def psycopg_sample(
        uow: PsycopgSyncUOW = Depends(Provide[PsycopgSyncContainer.psycopg_uow]),
):
    with uow as u:
        u.repository.create(...)
        
# some code
```
