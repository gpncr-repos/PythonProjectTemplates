# httpx

В проекте реализован синхронный и асинхронный клиент для интеграции по http.

## Прокси-клиент

Для инициализации клиента используется объекты прокси **HTTPSyncSession** и **HTTPAsyncSession**. Клиент инициализируется при создании прокси-объектов. Для закрытия используется отдельный метод `disconnect()`.

## Репозиторий

Репозитории **SyncHTTPRepository** и **AsyncHTTPRepository** реализованы в соответствии с интерфейсом **BaseRepository**. Каждый метод CRUD соответствует HTTP-методу. Метод `list()` остается непеопределенным.
Для репозитория написан декоратор для преобразования ответов на запросы **ResponseHandlerDecorator**. Он также может быть переопределен в соответствии с требуемой логикой.

## Контракты взаимодействия

Данные для запроса оборачиваются в объект **HTTPRequestDTO**, который содержит все необходимые для запроса поля. Ответ приходит в виде объекта **HTTPResponseDTO**, который содержит статус и ответ.

## UOW

Для взаимодействия с репозиторием рекомендуется использовать объект UOW, который используется в контекстном менеджере и закрывает http-клиент.

## DI-контейнер

Для инициализации объектов для работы с http-интеграции соблюдается следующая цепочка создания объектов в di-контейнере:

```python
http_sync_session = providers.Factory(HTTPSyncSession)
http_sync_repository = providers.Factory(SyncHTTPRepository, http_sync_session)
http_sync_uow = providers.Factory(SyncHTTPUOW, http_sync_repository)
```

Изначально создается объект прокси-соединения, который затем передается в объект репозитория.
Далее репозиторий используется для инициализации объекта UOW.

## Пример использования

```python
sync_container = HTTPSyncIntegrationContainer()
sync_uow = sync_container.http_sync_uow()

with sync_uow as uow:
    result = uow.repository.retrieve(
        HTTPRequestDTO(
            url="http://localhost:7777/api/posts",
            query_params={
                "id": 1
            }
        )
    )
```
