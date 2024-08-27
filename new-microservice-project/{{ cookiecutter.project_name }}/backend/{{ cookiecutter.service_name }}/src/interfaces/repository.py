# stdlib
import abc

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession



class AbstractAlchemyRepository(abc.ABC):
    """
    Базовый класс для репозитория Алхимии
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализировать переменные
        :param name: название репозитория
        :param session: сессия алхимии
        """

        self.session = session


class CreateMixin:
    """
    Миксин репозитория, содержащего метод create
    """

    @abc.abstractmethod
    def create(self, *args, **kwargs) -> any:
        """
        Создать записи
        """

        raise NotImplementedError


class RetrieveMixin:
    """
    Миксин репозитория, содержащего метод retrieve
    """

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs) -> any:
        """
        Получить записи
        """

        raise NotImplementedError


class UpdateMixin:
    """
    Миксин репозитория, содержащего метод update
    """

    @abc.abstractmethod
    def update(self, *args, **kwargs) -> any:
        """
        Обновить записи
        """

        raise NotImplementedError


class DeleteMixin:
    """
    Миксин репозитория, содержащего метод delete
    """

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> any:
        """
        Удалить записи
        """

        raise NotImplementedError
