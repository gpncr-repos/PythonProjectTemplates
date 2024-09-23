import abc

import httpx


class HTTPSyncSessionMaker(abc.ABC):
    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._client = httpx.Client()

    def get_client(self) -> httpx.Client:
        """
        Получить HTTP-клиент
        """

        return self._client


class HTTPAsyncSessionMaker(abc.ABC):
    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._client = httpx.AsyncClient()

    def get_client(self) -> httpx.AsyncClient:
        """
        Получить HTTP-клиент
        """

        return self._client
