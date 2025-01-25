import json
import logging
import time
import uuid

from fastapi import status as http_status
import starlette.middleware.base
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message, Scope

from tools.globals import g, set_extra_for_logs

logger = logging.getLogger(__name__)


def _bytes_to_json(source: bytes, encoding: str = "uft-8") -> bytes | str | dict| list:
    """
    Преобразовать тело запроса и ответа
    :param source: исходное тело запроса
    :param encoding: кодировка
    :return: копия source или результат преобразования этой копии
    """

    result = bytes(source)

    try:
        result = result.decode(encoding)
        result = json.loads(result)
    except Exception:
        pass

    return result


class RequestWithBody(Request):
    """
    Класс запроса с телом сообщения
    """

    def __init__(self, scope: Scope, body: bytes) -> None:
        """
        Инициализировать переменные
        :param scope: метаданные запроса
        :param body: тело запроса
        """

        super().__init__(scope, self._receive)
        self._body = body
        self._body_returned = False

    async def _receive(self) -> Message:
        """
        Получить данные запроса
        :return: словарь данных о запросе
        """

        if self._body_returned:
            return {
                "type": "http.disconnect"
            }
        else:
            self._body_returned = True

            return {
                "type": "http.request",
                "body": self._body,
                "more_body": False
            }


class LogRequestInfoMiddleware(starlette.middleware.base.BaseHTTPMiddleware):
    """
    Middleware для логирования информации о запросе, а также о теле запроса и теле ответа (в случае ошибки)
    """

    ERROR_HTTP_CODES = range(http_status.HTTP_400_BAD_REQUEST, http_status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED + 1)

    async def dispatch(
        self,
        request: Request,
        call_next: starlette.middleware.base.RequestResponseEndpoint
    ) -> Response:
        """
        Обработать запрос
        :param request: объект запроса
        :param call_next: коллбек запроса
        :return: ответ сервера
        """

        request_body_bytes = await request.body()
        request_with_body = RequestWithBody(request.scope, request_body_bytes)

        try:
            response = await call_next(request_with_body)
        except Exception:
            time1 = time.time()

            request_body = _bytes_to_json(request_body_bytes)
            request_total = round(time1 - g.extra_info_for_logs.get("_request_start", 0), 3)

            extra_kwargs = {
                "response_status": http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                "request_time": request_total
            }
            set_extra_for_logs(
                {
                    "request_body": request_body,
                    "response_body": None,
                    **extra_kwargs
                }
            )

            raise

        status = response.status_code

        time1 = time.time()
        request_total = round(time1 - g.extra_info_for_logs.get("_request_start", 0), 3)

        extra_kwargs = {
            "response_status": status,
            "request_time": request_total
        }

        if status in self.ERROR_HTTP_CODES:
            if isinstance(response, starlette.middleware.base._StreamingResponse):
                response_body_source = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body_source))
                response_body_bytes = b"".join(response_body_source)
            else:
                response_body_bytes = response.body

            response_body = _bytes_to_json(response_body_bytes)
            request_body = _bytes_to_json(request_body_bytes)

            extra_kwargs.update(
                {
                    "request_body": request_body,
                    "response_body": response_body
                }
            )

        set_extra_for_logs(extra_kwargs)

        return response


class SetRequestContextMiddleware:
    """
    Middleware для выставления глобальных параметров в контексте запроса
    """

    def __init__(self, app: starlette.middleware.base.BaseHTTPMiddleware) -> None:
        """
        Инициализировать переменные
        :param app: объект Middleware
        """

        self.app = app

    async def __call__(
        self,
        scope: dict[str, any],
        receive: starlette.types.Receive,
        send: starlette.types.Send
    ) -> None:
        """
        Выставить глобальные переменные в контексте запроса
        :param scope: метаданные запроса
        :param receive: объект управления жизненным циклом приложения при получении запроса
        :param send: объект управления жизненным циклом приложения при отправке ответа
        """

        if scope["type"] != "http":
            await self.app(scope, receive, send)

            return

        try:
            request = Request(scope, receive=receive)

            set_extra_for_logs(
                {
                    "request_id": uuid.uuid4(),
                    "_request_start": time.time(),
                    "method": request.method,
                    "url": request.url,
                    "base_url": request.base_url,
                    "query_params": request.query_params
                }
            )

            logger.debug("request started")
        except Exception as e:
            logger.error(f"Failed setting request context: {str(e)}")
        finally:
            set_extra_for_logs({})

        await self.app(scope, receive, send)
