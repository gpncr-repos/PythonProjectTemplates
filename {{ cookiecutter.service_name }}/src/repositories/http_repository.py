import json.decoder
import logging
from typing import Callable, Iterable

import httpx

from interfaces import base_repository
from models.dto import http_dto
from repositories import http_connection_proxy

logger = logging.getLogger(__name__)


class ResponseHandlerDecorator:
    """
    Класс, реализующий метод-декоратор для обработки HTTP-ответа
    """

    def _handle_sync(
        http_method: Callable[[http_dto.HTTPRequestDTO], httpx.Response]
    ) -> Callable:
        """
        Обработать синхронный http-запрос
        :param http_method: метод репозитория
        :return: функция-обертка
        """

        def execute_method(self, *args, **kwargs) -> any:
            """
            Выполнить метод репозитория
            """

            try:
                response = http_method(self, *args, **kwargs)
            except httpx.HTTPError as http_error:
                raise http_error
            except NotImplementedError as not_impl_error:
                raise not_impl_error
            except Exception as exception:
                raise exception

            try:
                payload = response.json()
            except json.decoder.JSONDecodeError as error:
                logger.error(str(error))
                payload = None

            return http_dto.HTTPResponseDTO(
                status=response.status_code,
                headers=dict(response.headers),
                payload=payload
            )

        return execute_method

    def _handle_async(
        http_method: Callable[[http_dto.HTTPRequestDTO], httpx.Response]
    ) -> Callable:
        """
        Обработать асинхронный http-запрос
        :param http_method: метод репозитория
        :return: функция-обертка
        """

        async def execute_method(self, *args, **kwargs) -> any:
            """
            Выполнить метод репозитория
            """

            try:
                response = await http_method(self, *args, **kwargs)
            except httpx.HTTPError as http_error:
                raise http_error
            except NotImplementedError as not_impl_error:
                raise not_impl_error
            except Exception as exception:
                raise exception

            try:
                payload = response.json()
            except json.decoder.JSONDecodeError as error:
                logger.error(str(error))
                payload = None

            return http_dto.HTTPResponseDTO(
                status=response.status_code,
                headers=dict(response.headers),
                payload=payload
            )

        return execute_method

    handle_sync = staticmethod(_handle_sync)
    handle_async = staticmethod(_handle_async)


class SyncHTTPRepository(base_repository.BaseRepository):
    """
    Репозиторий для синхронных HTTP-запросов
    """

    def __init__(self, http_client: http_connection_proxy.HTTPSyncSession) -> None:
        """
        Инициализировать переменные
        :param http_client: HTTP-клиент
        """

        self.client = http_client.connect()

    @ResponseHandlerDecorator.handle_sync
    def create(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return self.client.post(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
            json=request_params.payload,
            data=request_params.form_data,
        )

    @ResponseHandlerDecorator.handle_sync
    def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return self.client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )


    @ResponseHandlerDecorator.handle_sync
    def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    @ResponseHandlerDecorator.handle_sync
    def update(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return self.client.patch(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
            json=request_params.payload,
            data=request_params.form_data,
        )

    @ResponseHandlerDecorator.handle_sync
    def delete(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать DELETE-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return self.client.delete(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )


class AsyncHTTPRepository(base_repository.BaseRepository):
    """
    Репозиторий для асинхронных HTTP-запросов
    """

    def __init__(self, http_client: http_connection_proxy.HTTPAsyncSession) -> None:
        """
        Инициализировать переменные
        :param http_client: HTTP-клиент
        """

        self.client = http_client.connect()

    @ResponseHandlerDecorator.handle_async
    async def create(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return await self.client.post(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
            json=request_params.payload,
            data=request_params.form_data,
        )

    @ResponseHandlerDecorator.handle_async
    async def retrieve(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return await self.client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )

    @ResponseHandlerDecorator.handle_async
    async def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    @ResponseHandlerDecorator.handle_async
    async def update(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать PATCH-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return await self.client.patch(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
            json=request_params.payload,
            data=request_params.form_data,
        )

    @ResponseHandlerDecorator.handle_async
    async def delete(self, request_params: http_dto.HTTPRequestDTO) -> httpx.Response:
        """
        Сделать DELETE-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        return await self.client.delete(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )
