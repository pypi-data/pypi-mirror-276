import http
import json
import logging
import math
import time
from logging import ERROR, INFO, WARNING
from typing import Any, Dict, Optional

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import Message

EMPTY_VALUE = ""


class Middleware:
    def __init__(self) -> None:
        Middleware.reset_logging_handlers()

    async def _log(
        self,
        level: int,
        message: str,
        extra_fields: Dict[str, Any],
        exception_object: Optional[Exception],
    ):
        raise NotImplementedError()

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint, *args, **kwargs
    ):
        start_time = time.time()
        exception_object = None

        # Request Side
        try:
            raw_request_body = await request.body()
            await Middleware.set_body(request, raw_request_body)
            raw_request_body = await Middleware.get_body(request)
            request_body = raw_request_body.decode()
        except Exception:
            request_body = EMPTY_VALUE

        server: tuple = request.get("server", ("localhost", 9090))
        request_headers: dict = dict(request.headers.items())

        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = b""
            async for chunk in response.body_iterator:  # type: ignore
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        duration: int = math.ceil((time.time() - start_time) * 1000)

        # Initialization and formation of fields for request-response
        extra_fields = dict(
            request_uri=str(request.url),
            request_protocol=await Middleware.get_protocol(request),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f"{server[0]}:{server[1]}",
            request_size=int(request_headers.get("content-length", 0)),
            request_content_type=request_headers.get("content-type", EMPTY_VALUE),
            request_headers=json.dumps(request_headers),
            request_body=request_body,
            remote_host=f"{request.client[0]}:{request.client[1]}",
            response_status_code=response.status_code,
            response_size=int(response_headers.get("content-length", 0)),
            response_headers=json.dumps(response_headers),
            response_body=response_body.decode(),
            duration=duration,
        )

        if exception_object:
            level = ERROR
        elif 0 <= response.status_code <= 299:
            level = INFO
        elif 300 <= response.status_code <= 399:
            level = WARNING
        else:
            level = ERROR

        message = (
            f"{'Error' if level == ERROR else 'Response'} "
            f"with code {response.status_code} "
            f"for request {request.method} {str(request.url)}"
        )

        await self._log(
            level=level,
            message=message,
            extra_fields=extra_fields,
            exception_object=exception_object,
        )
        return response

    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return EMPTY_VALUE

    @staticmethod
    async def get_body(request: Request) -> bytes:
        body = await request.body()
        await Middleware.set_body(request, body)
        return body

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> Message:
            return {"type": "http.request", "body": body}

        request._receive = receive

    @staticmethod
    def reset_logging_handlers() -> None:
        """Remove all default fastapi and gunicorn loggers."""
        loggers = (
            logging.getLogger(name)
            for name in logging.root.manager.loggerDict
            if name.startswith(("uvicorn.", "gunicorn."))
        )
        for logger in loggers:
            logger.handlers = []


class LoggingMiddleware(Middleware):
    """Logging Malware with support for logging module"""

    def __init__(self, logger_name: str, reload_logger_: bool = True) -> None:
        super().__init__()

        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.reload_logger_ = reload_logger_

    def _get_logger(self):
        if self.reload_logger_:
            return logging.getLogger(self.logger_name)
        return self.logger

    async def _log(
        self,
        level: int,
        message: str,
        extra_fields: Dict[str, Any],
        exception_object: Exception,
    ):
        self._get_logger().log(
            level,
            message,
            extra=extra_fields,
            exc_info=exception_object,
        )
