import traceback

from app.domain.usecases.load_account_by_token import LoadAccountByToken
from app.main.decorators.log import log_controller_handler
from ..protocols.http import HttpRequest, HttpResponse
from ..protocols.middlewares import Middleware
from ..helpers.http.http_herlper import forbidden, ok, server_error
from ..errors.access_danied_error import AccessDaniedError
from ..errors.server_error import ServerError


class AuthMiddleware(Middleware):
    def __init__(self, load_account_by_token: LoadAccountByToken):
        self._load_account_by_token = load_account_by_token

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            access_token = (
                request.headers and request.headers.get("x-access-token") or None
            )
            if access_token:
                account = self._load_account_by_token.load_by_token(
                    access_token=access_token
                )
                if account:
                    return ok(account.id)

            return forbidden(AccessDaniedError())
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
