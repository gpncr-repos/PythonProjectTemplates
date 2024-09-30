from typing import Callable

import httpx

from models.dto import http_dto
from interfaces import base_http_session_maker, base_repository


class ErrorCatcherDecorator:
    """
    Класс, реализующий метод-декоратор для отлавливания ошибок в репозитории
    """

    def _catch_sync_exception(http_method: Callable) -> Callable:
        """
        Отловить ошибку при синхронном http-запросе
        :param http_method: метод репозитория
        :return: функция-обертка
        """

        def execute_method(self, *args, **kwargs) -> any:
            """
            Выполнить метод репозитория
            """

            try:
                return http_method(self, *args, **kwargs)
            except httpx.HTTPError as http_error:
                raise http_error
            except NotImplementedError as not_impl_error:
                raise not_impl_error

        return execute_method

    def _catch_async_exception(http_method: Callable) -> Callable:
        """
        Отловить ошибку при асинхронном http-запросе
        :param http_method: метод репозитория
        :return: функция-обертка
        """

        async def execute_method(self, *args, **kwargs) -> any:
            """
            Выполнить метод репозитория
            """

            try:
                return await http_method(self, *args, **kwargs)
            except httpx.HTTPError as http_error:
                raise http_error
            except NotImplementedError as not_impl_error:
                raise not_impl_error

        return execute_method

    catch_sync_exception = staticmethod(_catch_sync_exception)
    catch_async_exception = staticmethod(_catch_async_exception)


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

    @ErrorCatcherDecorator.catch_sync_exception
    def create(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

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

    @ErrorCatcherDecorator.catch_sync_exception
    def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        result = self.client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )

        return http_dto.HTTPResponseDTO(
            status=result.status_code,
            payload=result.json()
        )

    @ErrorCatcherDecorator.catch_sync_exception
    def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    @ErrorCatcherDecorator.catch_sync_exception
    def update(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

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

    @ErrorCatcherDecorator.catch_sync_exception
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

    @ErrorCatcherDecorator.catch_async_exception
    async def create(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

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

    @ErrorCatcherDecorator.catch_async_exception
    async def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        result = await self.client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )

        return http_dto.HTTPResponseDTO(
            status=result.status_code,
            payload=result.json()
        )

    @ErrorCatcherDecorator.catch_async_exception
    async def list(self, *args, **kwargs) -> list[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    @ErrorCatcherDecorator.catch_async_exception
    async def update(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

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

    @ErrorCatcherDecorator.catch_async_exception
    async def delete(self, *args, **kwargs) -> any:
        """
        Удалить запись
        """

        return super().delete(*args, **kwargs)
