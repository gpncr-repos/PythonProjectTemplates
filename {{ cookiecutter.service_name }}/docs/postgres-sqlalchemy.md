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

Нашей рекомендацией является использование репозитория вместе с **UOW**, т.к. в таком случае **UOW** полностью контролирует время жизни транзакций.  Однако, если вы решили использовать репозиторий отдельно, то минимальное требование к его правильной работе - наличие прокси-объекта соединения, которое прокидывается в инициализатор репозитория.

После инициализации объекта репозитория при каждом запросе в БД требуется получать объект сессии из прокси-объекта соединения. В данной реализации объект сессии будет всегда одним и тем же.

```python
from repositories import base_alchemy_repository

class TestRepository(base_alchemy_repository.BaseAlchemyRepository):
    # Остальной код

    def create(self, *args, **kwargs) -> None:
        session = self.connection_proxy.connect()
        
        # Инициализируем объект ORM
        db_model = ...

        session.add(db_model)
        session.commit()
    
    # Остальной код
```

## Unit of Work (UOW)

Для обеспечения транзакционности работы с базой данных PostgreSQL были написаны два класса Unit of Work (UOW) для синхронной и асинхронной реализаций.

Класс UOW функционирует как контекстный менеджер и в методе `__exit__()` вызывает:
- `commit()`: для подтверждения транзакции.
- `rollback()`: для отката транзакции в случае возникновения исключений.

## DI-контейнер

Для инициализации объекта UOW и работы с базой данных PostgreSQL используется DI-контейнер.
Пример создания объектов в DI-контейнере:

```python
class AlchemySyncContainer(containers.DeclarativeContainer):
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
# Остальной код

@inject
def psycopg_example(
    uow: AlchemySyncUOW = Provide[AlchemySyncContainer.uow]
):
    with uow as u:
        u.repository.create(...)
        u.commit()

# Остальной код

container = AlchemySyncContainer()
engine = container.engine_factory().create()
engine.dispose()
```

Особое внимание в этом примере надо обратить на явное закрытие соединения с БД пользователем через объект движка и на метод `create()`. Несмотря на название, он возвращает один и тот же движок, т.к. фабрика движков является Синглотоном.

## Тестирование

Для тестирования предлагается использовать мок для основного взаимодействия с БД - с помощью сессии.

В общем случае полный мок для БД выглядят так:

```python
def _mock(self):
    """
    Сделать моковое взаимодействие с БД
    """

    deletion = self._session.delete

    async def mock_delete(instance):
        insp = inspect(instance)

        if not insp.persistent:
            self._session.expunge(instance)
        else:
            await deletion(instance)

        return await asyncio.sleep(0)

    self._session.commit = MagicMock(side_effect=self._session.flush)
    self._session.delete = MagicMock(side_effect=mock_delete)
```

Здесь происходит мок сразу двух методов - commit и delete. Commit заменяется на flush, что позволяет не заканчивать транзакцию и не записывать данные в реальную БД. Delete же просто настроен на очищение объектов в текущей сессии.

Такая логика мока может быть записана в класс прокси-подключения к БД. Для этого были созданы классы **AlchemyTestSyncConnectionProxy** и **AlchemyTestAsyncConnectionProxy** (**storage/sqlalchemy/connection_proxy.py**). В них также сразу инициализируется движок, который будет актуален лишь на один тест и не сможет переиспользоваться. Для отключения от БД используется закрытие сессии close() и возвращение ее в пул соединений с помощью метода движка dispose().

```python
def __init__(
    self,
    engine_factory: alchemy_engine_factory.AlchemyEngineFactoryBase,
) -> None:
    """
    Инициализировать переменные
    """

    super().__init__(engine_factory)

    self._engine = create_async_engine(
        str(pg_config_.postgres_async_dsn),
        pool_size=pg_config_.connection_pool_size,
        echo=True
    )
    self._session_maker = sessionmaker(  # noqa
        autocommit=False,
        autoflush=False,
        bind=self._engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

async def disconnect(self) -> None:
    """
    Разорвать соединение с БД
    """

    await self._session.close()
    await self._engine.dispose()
```

Мы рекомендуем пользоваться объектами репозиториев вместе с UOW, поэтому надо сразу подружить наши UOW с новым типом прокси-подключения. Для этого достаточно сразу инициализировать объект сессии и переопределить ее в объекте репозитория.

```python
def __init__(self, repository: base_alchemy_repository.BaseAlchemyRepository):
    """
    Инициализировать переменные
    :param repository: репозиторий
    """

    super().__init__(repository)

    self._session = self.repository.connection_proxy.connect()
    self.repository.connection_proxy.connect = MagicMock(side_effect=lambda: self._session)
```

При открытии и закрытии контекстного менеджера дополнительная логика работы с транзакциями не понадобится, т.к. мы замокали взаимодействие с БД.

Для коммита изменений достаточно вызвать замоканный commit(), а для отката - сделать rollback().

Готовые тестовые UOW реализованы для синхронного (**TestAlchemySyncUOW**) и асинхронного (**TestAlchemyAsyncUOW**) взаимодействия и находятся в модуле **uows/alchemy_uow.py**.

Рассмотрим пример использования тестовых прокси-соединения и UOW. Представим, что у нас есть слой сервиса **CompanyService**, у которого есть метод **create_company()**, его логика взаимодействует с БД и ее надо проверить:

```python
class CompanyService:
    @inject
    async def create_company(self, company: Company, uow: AlchemyAsyncUOW = Provide[AlchemyAsyncContainer.company_uow]) -> None:
        """Создание компании"""
        async with uow:
            await uow.repository.create(company)
            await uow.commit()
```

Здесь в качестве аргументов мы получаем агрегат компании и инъектируемый UOW.

Посмотрим на DI-контейнеры.

```python
class AlchemyAsyncContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через асинхронную сессию Алхимии
    """

    # Указать связанные модули
    wiring_config = containers.WiringConfiguration(packages=["services"])

    engine_factory = providers.Factory(
        alchemy_engine_factory.AlchemyAsyncEngineFactory,
        config.postgres_async_dsn,
        config.connection_pool_size,
    )

    connection_proxy = providers.Factory(
        connection_proxy_.AlchemyAsyncConnectionProxy, engine_factory
    )
    test_connection_proxy = providers.Factory(
        connection_proxy_.AlchemyTestAsyncConnectionProxy, engine_factory
    )

    # Добавить провайдеры конкретных реализаций репозиториев
    company_repository = providers.Factory(company_repository_.CompanyRepository, connection_proxy)

    # Добавить провайдеры конкретных реализаций UOW
    company_uow = providers.Factory(alchemy_uow.AlchemyAsyncUOW, company_repository)
    company_test_uow = providers.Singleton(alchemy_uow.TestAlchemyAsyncUOW, company_repository)

class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с сервисами
    """

    # Указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    # Добавить провайдеры конкретных реализаций сервисов
    company_service = providers.Factory(company_service.CompanyService)
```

Здесь стоит обратить внимание на контейнер **AlchemyAsyncContainer**. Помимо необходимых провайдеров для реальной работы с БД здесь добавлены провайдеры **test_connection_proxy** и **company_test_uow**, которые организуют моковое взаимодействие с БД. **company_test_uow** является синглтоном, т.к. он должен переиспользоваться внутри одного и того же теста, потому что он содержит объекты для соединения с БД в рамках одного теста.

Теперь необходимо подготовить фикстуры для нашего теста.

```python
@pytest_asyncio.fixture
async def alchemy_async_container():
    """
    Получить DI-контейнер с провайдерами асинхронной Алхимии
    """

    container_ = alchemy_container.AlchemyAsyncContainer()
    container_.wire(modules=[__name__])
    container_.connection_proxy.override(container_.test_connection_proxy)
    container_.company_uow.override(container_.company_test_uow)

    yield container_

    await container_.company_test_uow().rollback()
    container_.unwire()


@pytest.fixture
def service_container(alchemy_async_container):  # noqa
    """
    Получить DI-контейнер с провайдерами сервисов
    """

    container_ = service_container_.ServiceContainer()
    container_.wire(modules=[__name__])

    yield container_

    container_.unwire()
```

Фикстура **alchemy_async_container()** отвечает за получение DI-контейнера для работы с провайдерами Алхимии. Здесь мы делаем override прокси-соединения для реальной работы с БД нашим тестовым прокси-соединением, реализованного с помощью моков. Также overrride происходит с объектом UOW - его мы заменяем на тестовый UOW, который потом будет использоваться в сервисе **CompanyService**. Для отката всех сделанных коммитов в конце каждого теста используется **rollback()** из объекта UOW.

Фикстура **service_container()** просто получает объект сервиса.

Обе фикстуры делают wire для правильной работы с тестовым модулем и последующий unwire.

Имея на руках фикстуры, можно приступить к написанию теста:

```python
@pytest.mark.asyncio
async def test_create_company(service_container):
    service = service_container.company_service()

    user_info = value_objects.UserInfo(
        email="tech_company@example.com",
        name="Tech Solutions Inc.",
        hashed_password="secure_hash",
        is_company=True,
        created_at=datetime.datetime.now()
    )
    company_id = uuid.uuid4()
    company = aggregate_roots.Company(id_=company_id, user_info=user_info)

    await service.create_company(company)
    retrieved_company = await service.get_company(company_id)

    assert company_id == retrieved_company.id
```

В тесте мы получаем объект сервиса, у которого вызываем тестируемый метод с начальными параметрами. Т.к. мы замокали объект UOW в фикстурах, работа будет происходить с нашим тестовым UOW.
