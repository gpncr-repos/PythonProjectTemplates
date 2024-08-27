import abc


class DomainModelObject(abc.ABC):
    """
    Базовый класс для объекта доменной модели
    """

    pass


class DomainRoot(DomainModelObject):
    """
    Базовый класс для root домена
    """

    pass


class DomainEntity(DomainModelObject):
    """
    Базовый класс для entity домена
    """

    pass


class DomainValueObject(DomainModelObject):
    """
    Базовый класс для value object домена
    """

    pass
