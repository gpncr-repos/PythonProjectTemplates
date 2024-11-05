# stdlib
import abc


class BaseRawSQLCreator(abc.ABC):
    """
    Абстракция с методами для создания sql-query
    """

    @abc.abstractmethod
    def make_insert_query(self, *args, **kwargs):
        """
        Сформировать sql строку для создания записи в таблицу
        """
        ...

    @abc.abstractmethod
    def make_select_query(self, *args, **kwargs):
        """
        Сформировать sql строку для получения записей из таблицы
        """
        ...

    @abc.abstractmethod
    def make_update_query(self, *args, **kwargs):
        """
        Сформировать sql строку для обновления записей таблицы
        """
        ...

    @abc.abstractmethod
    def make_delete_query(self, *args, **kwargs):
        """
        Сформировать sql строку для удаления записей из таблицы
        """
        ...
