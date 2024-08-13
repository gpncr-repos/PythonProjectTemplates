# stdlib
import abc

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(abc.ABC):
    """
    Абстрактный класс репозитория
    """

    def __init__(self, name: str) -> None:
        """
        Конструктор
        :param name: название репозитория
        """

        self.name = name


class AlchemyRepository(AbstractRepository):
    """
    Базовый класс для репозитория Алхимии
    """

    def __init__(self, name: str, session: AsyncSession) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        :param session: сессия алхимии
        """

        self.session = session
        super().__init__(name)
