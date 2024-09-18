from dependency_injector import containers, providers

from interfaces.base_session import BaseSession



class RepositoriesContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["web.entrypoints"])

    db = providers.AbstractFactory(BaseSession)
