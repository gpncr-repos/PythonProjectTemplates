import httpx

from interfaces import base_proxy


class HTTPSyncSession(base_proxy.ConnectionProxy):
    """
    Синхронный клиент httpx
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._client = httpx.Client()

    def connect(self) -> httpx.Client:
        """
        Получить HTTP-клиент
        """

        return self._client

    def disconnect(self) -> None:
        """
        Отключить HTTP-клиент
        """

        self._client.close()


class HTTPAsyncSession(base_proxy.ConnectionProxy):
    """
    Синхронный клиент httpx
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._client = httpx.AsyncClient()

    def connect(self) -> httpx.AsyncClient:
        """
        Получить HTTP-клиент
        """

        return self._client

    async def disconnect(self) -> None:
        """
        Отключить HTTP-клиент
        """

        await self._client.aclose()
