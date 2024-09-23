import httpx

from models.dto import http_dto
from interfaces import base_http_session_maker, base_repository


class SyncHTTPRepository(base_repository.BaseRepository):
    """
    Репозиторий для синхронных HTTP-запросов
    """

    def __init__(self, http_client: base_http_session_maker.HTTPSyncSessionMaker) -> None:
        """
        Инициализировать переменные
        :param http_client: HTTP-клиент
        """

        self.client = http_client.get_client()

    def create(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            result = self.client.post(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload
            )

            return http_dto.HTTPResponseDTO(
                status=result.status_code,
                payload=result.json()
            )
        except httpx.HTTPError as error:
            raise error

    def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            result = self.client.get(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params
            )

            return http_dto.HTTPResponseDTO(
                status=result.status_code,
                payload=result.json()
            )
        except httpx.HTTPError as error:
            raise error

    def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    def update(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            result = self.client.patch(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload
            )

            return http_dto.HTTPResponseDTO(
                status=result.status_code,
                payload=result.json()
            )
        except httpx.HTTPError as error:
            raise error

    def delete(self, *args, **kwargs) -> any:
        """
        Удалить запись
        """

        return super().delete(*args, **kwargs)


class AsyncHTTPRepository(base_repository.BaseRepository):
    """
    Репозиторий для асинхронных HTTP-запросов
    """

    def __init__(self, http_client: base_http_session_maker.HTTPAsyncSessionMaker) -> None:
        """
        Инициализировать переменные
        :param http_client: HTTP-клиент
        """

        self.client = http_client.get_client()

    async def create(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            result = await self.client.post(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload
            )

            return await http_dto.HTTPResponseDTO(
                status=result.status_code,
                payload=result.json()
            )
        except httpx.HTTPError as error:
            raise error

    async def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            result = await self.client.get(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params
            )

            return http_dto.HTTPResponseDTO(
                status=result.status_code,
                payload=result.json()
            )
        except httpx.HTTPError as error:
            raise error

    async def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    async def update(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        try:
            result = await self.client.patch(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload
            )

            return http_dto.HTTPResponseDTO(
                status=result.status_code,
                payload=result.json()
            )
        except httpx.HTTPError as error:
            raise error

    async def delete(self, *args, **kwargs) -> any:
        """
        Удалить запись
        """

        return super().delete(*args, **kwargs)
