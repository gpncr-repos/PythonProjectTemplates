# thirdparty
from dependency_injector import containers

# project
from config import pg_config

config = pg_config.pg_config


class DomainContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с доменными моделями
    """

    # Указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=None)

    # Добавить провайдеры конкретных реализаций доменных моделей
    ...
