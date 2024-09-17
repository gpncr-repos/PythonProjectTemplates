import strawberry


@strawberry.type
class IndexType:
    """
    Тип данных информации о сервисе
    """

    project_name: str
    app_name: str
    app_version: str
