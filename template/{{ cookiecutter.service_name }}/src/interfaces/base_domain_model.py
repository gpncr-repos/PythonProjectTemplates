import abc


class DomainAggregate(abc.ABC):
    """
    Базовый класс агрегата
    """

    pass


class DomainValueObject(abc.ABC):
    """
    Базовый класс для value object домена
    """

    pass


class DomainEntityObject(abc.ABC):
    """
    Базовый класс для entity домена
    """

    pass
