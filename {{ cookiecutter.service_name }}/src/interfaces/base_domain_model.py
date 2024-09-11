import abc


class DomainModelObject(abc.ABC):
    """
    Базовый класс для объекта доменной модели
    """

    pass


class DomainAggregate(DomainModelObject, abc.ABC):
    """
    Базовый класс агрегата
    """

    pass


class DomainValueObject(DomainModelObject, abc.ABC):
    """
    Базовый класс для value object домена
    """

    pass


class DomainEntityObject(DomainModelObject, abc.ABC):
    """
    Базовый класс для entity домена
    """

    pass
