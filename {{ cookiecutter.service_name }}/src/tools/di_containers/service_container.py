# thirdparty
from dependency_injector import containers

# project
from config import pg_config

config = pg_config.pg_config


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с сервисами
    """

    # Указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    # Добавить провайдеры конкретных реализаций сервисов
    ...
