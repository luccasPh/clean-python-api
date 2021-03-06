from ..protocols.http import HttpRequest, HttpResponse
from ..protocols.middlewares import Middleware
from ..helpers.http.http_herlper import forbidden
from ..errors.access_danied_error import AccessDaniedError


class AuthMiddleware(Middleware):
    def handle(self, request: HttpRequest) -> HttpResponse:
        return forbidden(AccessDaniedError())
