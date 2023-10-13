import uuid
from django_structlog.middlewares import RequestMiddleware
import json
import structlog
from django_structlog import signals

logger = structlog.getLogger("middleware")


def get_request_header(request, header_key, meta_key):
    if hasattr(request, "headers"):
        return request.headers.get(header_key)

    return request.META.get(meta_key)


class LoggerMiddleware(RequestMiddleware):
    def _get_response_body(self, response):
        if getattr(response, "streaming", False):
            response_body = "** Streaming **"
        else:
            if type(response.content) == bytes:
                response_body = json.loads(response.content.decode())
            else:
                response_body = json.loads(response.content)

        return response_body

    def prepare(self, request):
        from ipware import get_client_ip

        request_id = get_request_header(
            request, "x-request-id", "HTTP_X_REQUEST_ID"
        ) or str(uuid.uuid4())
        correlation_id = get_request_header(
            request, "x-correlation-id", "HTTP_X_CORRELATION_ID"
        )
        structlog.contextvars.bind_contextvars(request_id=request_id)
        self.bind_user_id(request)
        if correlation_id:
            structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        ip, _ = get_client_ip(request)
        structlog.contextvars.bind_contextvars(ip=ip)
        signals.bind_extra_request_metadata.send(
            sender=self.__class__, request=request, logger=logger
        )
        logger.info(
            "request_started",
            request=self.format_request(request),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        self._raised_exception = False
        request.id = request_id

    def __call__(self, request):
        response = super().__call__(request)
        response["x-request-id"] = request.id
        response["x-correlation-id"] = request.id
        if response.get("content-type") in (
            "application/json",
            "application/vnd.api+json",
        ):
            ...
            # response_body = self._get_response_body(response)
        return response
