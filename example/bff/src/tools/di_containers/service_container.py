# thirdparty
from dependency_injector import containers, providers

from services import calculator_service


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с сервисами
    """

    # указать связанные модули
    wiring_config = containers.WiringConfiguration(modules=["web.entrypoints.calc_oil_entrypoint"])

    # Добавить провайдеры конкретных реализаций сервисов
    calculator_service = providers.Factory(calculator_service.CalculatorService)
