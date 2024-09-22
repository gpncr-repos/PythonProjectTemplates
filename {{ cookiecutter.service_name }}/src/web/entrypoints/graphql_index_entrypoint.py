import strawberry
from strawberry.fastapi import GraphQLRouter

from config import app_config
from web.schemas import index_schema as schema

config = app_config.app_config

@strawberry.type
class IndexQuery:
    """
    Класс запроса через GraphQL на получение данных
    """

    @strawberry.field
    async def get_app_info(self) -> schema.IndexType:
        """
        Получить информацию о приложении
        :return: информация о приложении
        """

        return schema.IndexType(
            project_name=config.project_name,
            app_name=config.app_name,
            app_version=config.app_version
        )


index_schema = strawberry.Schema(query=IndexQuery)
router = GraphQLRouter(index_schema, "/")
